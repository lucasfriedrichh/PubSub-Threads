import pickle
import socket
import threading
import time
from message import Message, ControlMessage

# Global variables
message_lists = {tipo: [] for tipo in range(1, 7)}  # Messages per type (types 1 to 6)
message_conditions = {tipo: threading.Condition() for tipo in range(1, 7)}  # Condition per type
stop_event = threading.Event()  # Event to signal threads to stop
seq_numbers = {tipo: 0 for tipo in range(1, 7)}  # Per-type sequence numbers
seq_locks = {tipo: threading.Lock() for tipo in range(1, 7)}  # Lock per type for seq_numbers

def listener_thread():
    """Thread that listens to messages from geradores and saves them into per-type lists."""
    HOST = ''
    PORT = 1682  # UDP port for receiving messages from geradores

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind((HOST, PORT))
    udp.settimeout(1.0)  # Set a timeout to periodically check for stop_event

    while not stop_event.is_set():
        try:
            msg_bytes, client = udp.recvfrom(4096)
            try:
                message = pickle.loads(msg_bytes)
                tipo = message.tipo

                # Update per-type sequence number
                with seq_locks[tipo]:
                    seq = seq_numbers[tipo]
                    seq_numbers[tipo] += 1
                message.seq = seq  # Update the sequence number in the message

                print(f"Received message from {client}")
                print(f"Message: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")

                # Add the message to the per-type list and notify waiting consumers
                with message_conditions[tipo]:
                    message_lists[tipo].append(message)
                    message_conditions[tipo].notify_all()  # Notify consumers waiting for this type
            except Exception as e:
                print(f"An error occurred while processing the message: {e}")
                continue
        except socket.timeout:
            continue  # Continue the loop to check for stop_event
        except Exception as e:
            print(f"An error occurred while receiving data: {e}")
            continue

    udp.close()
    print("Listener thread terminated.")

def consumer_acceptor_thread():
    """Thread that accepts connections from consumers and creates threads to serve them."""
    HOST = ''
    PORT = 1683  # TCP port for consumer connections

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server.bind((HOST, PORT))
    tcp_server.listen()
    tcp_server.settimeout(1.0)  # Set timeout to check for stop_event

    print(f"Consumer acceptor thread started, listening on port {PORT}")

    while not stop_event.is_set():
        try:
            client_socket, client_address = tcp_server.accept()
            print(f"Consumer connected from {client_address}")
            # Create a thread to serve this consumer
            threading.Thread(target=consumer_thread, args=(client_socket,), daemon=True).start()
        except socket.timeout:
            continue  # Continue to check for stop_event
        except Exception as e:
            print(f"Error accepting consumer connection: {e}")
            continue

    tcp_server.close()
    print("Consumer acceptor thread terminated.")

def consumer_thread(client_socket):
    """Thread to serve a connected consumer."""
    stop_consumer_event = threading.Event()
    desired_types_lock = threading.Lock()
    desired_types = []
    last_seq_sent = {}

    def receive_commands():
        """Thread to receive commands from the client."""
        try:
            while not stop_consumer_event.is_set():
                data = client_socket.recv(4096)
                if not data:
                    # Connection closed
                    print("Client closed the connection.")
                    stop_consumer_event.set()
                    break
                # Process the message
                control_message = pickle.loads(data)
                if isinstance(control_message, ControlMessage):
                    if control_message.command == 'change_type':
                        new_desired_types = control_message.data
                        if not isinstance(new_desired_types, list) or not all(isinstance(t, int) for t in new_desired_types):
                            print("Invalid desired types received from consumer.")
                            stop_consumer_event.set()
                            break
                        with desired_types_lock:
                            desired_types.clear()
                            desired_types.extend(new_desired_types)
                            for tipo in new_desired_types:
                                if tipo not in last_seq_sent:
                                    last_seq_sent[tipo] = -1
                        print(f"Consumer changed desired types to: {desired_types}")
                    else:
                        print(f"Unknown control command: {control_message.command}")
                else:
                    print("Received unknown data from consumer.")
        except Exception as e:
            print(f"Error receiving data from consumer: {e}")
            stop_consumer_event.set()

    def send_messages():
        """Thread to send messages to the client."""
        try:
            while not stop_consumer_event.is_set():
                with desired_types_lock:
                    current_desired_types = desired_types.copy()
                for tipo in current_desired_types:
                    with message_conditions[tipo]:
                        # Wait for new messages or timeout
                        message_conditions[tipo].wait(timeout=1.0)
                        # Send new messages
                        messages = message_lists[tipo]
                        for message in messages:
                            if message.seq > last_seq_sent.get(tipo, -1):
                                # Send the message to the consumer
                                try:
                                    client_socket.sendall(pickle.dumps(message))
                                except Exception as e:
                                    print(f"Error sending message to consumer: {e}")
                                    stop_consumer_event.set()
                                    return
                                last_seq_sent[tipo] = message.seq
                time.sleep(0.1)  # Avoid tight loop
        except Exception as e:
            print(f"Error in send_messages thread: {e}")
            stop_consumer_event.set()

    try:
        # Receive the initial desired types from the consumer
        data = client_socket.recv(4096)
        desired_types = pickle.loads(data)
        if not isinstance(desired_types, list) or not all(isinstance(t, int) for t in desired_types):
            print("Invalid desired types received from consumer.")
            client_socket.close()
            return
        print(f"Consumer requested types: {desired_types}")

        last_seq_sent = {tipo: -1 for tipo in desired_types}

        # Send existing messages of the desired types
        for tipo in desired_types:
            with message_conditions[tipo]:
                messages = message_lists[tipo]
                for message in messages:
                    if message.seq > last_seq_sent[tipo]:
                        # Send the message to the consumer
                        try:
                            client_socket.sendall(pickle.dumps(message))
                        except Exception as e:
                            print(f"Error sending message to consumer: {e}")
                            return
                        last_seq_sent[tipo] = message.seq

        # Start the receive_commands and send_messages threads
        recv_thread = threading.Thread(target=receive_commands)
        send_thread = threading.Thread(target=send_messages)
        recv_thread.start()
        send_thread.start()

        # Wait for both threads to finish
        recv_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error in consumer thread: {e}")
    finally:
        client_socket.close()
        print("Consumer thread terminated.")

def main():
    # Start the listener_thread to receive messages from geradores
    listener = threading.Thread(target=listener_thread)
    listener.start()

    # Start the consumer acceptor thread to accept consumer connections
    consumer_acceptor = threading.Thread(target=consumer_acceptor_thread)
    consumer_acceptor.start()

    # Wait for the user to press enter to stop the difusor
    input("Pressione enter para encerrar o difusor!\n")
    print("Encerrando o difusor...")
    stop_event.set()

    # Ensure the listener and acceptor threads have finished
    listener.join()
    consumer_acceptor.join()

    print("\nDifusor finalizado.")

if __name__ == '__main__':
    main()

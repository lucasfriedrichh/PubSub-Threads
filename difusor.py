import pickle
import socket
import threading
from message import Message 

HOST = ''
PORT = 1682

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind((HOST, PORT))

stop_event = threading.Event()  # Event to signal threads to stop

def input_thread():
    """Thread that waits for the user to press enter to stop the difusor."""
    input("Pressione enter para encerrar o difusor!\n")
    print("Encerrando o difusor...")
    stop_event.set()

def main():
    seq_numbers = {}
    udp.settimeout(1.0)
    
    # Thread to kill difusor
    threading.Thread(target=input_thread, daemon=True).start()

    first_run = True  # Flag to control when to print the waiting message

    while not stop_event.is_set():
        if first_run:
            print('\nWaiting for the message ...')
            first_run = False  # Reset the flag after printing

        try:
            msg_bytes, client = udp.recvfrom(4096)  # Adjust buffer size if necessary
            try:
                message = pickle.loads(msg_bytes)
                tipo = message.tipo
                seq = seq_numbers.get(tipo, 0) + 1
                seq_numbers[tipo] = seq
                message.seq = seq  # Update the sequence number if needed
                print(f"Received message from {client}")
                print(f"Message: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")

                first_run = True  # Set the flag to print the waiting message next time
            except Exception as e:
                print(f"An error occurred while processing the message: {e}")
                continue
        except socket.timeout:
            # Do not set first_run to True here to avoid printing the message repeatedly
            continue
        except Exception as e:
            print(f"An error occurred while receiving data: {e}")
            continue

    udp.close()
    print("Difusor finalizado.")

if __name__ == '__main__':
    main()

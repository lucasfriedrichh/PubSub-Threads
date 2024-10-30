import socket
import threading
import pickle
import time
from message import Message, ControlMessage  # Ensure ControlMessage is defined

HOST = '127.0.0.1'  # Difusor's IP address
PORT = 1683         # TCP port used by the difusor
stop_event = threading.Event()
quit_event = threading.Event()

def receive_messages(sock, stop_event):
    """Thread function to receive messages from the difusor."""
    while not stop_event.is_set():
        try:
            data = sock.recv(4096)
            if not data:
                # Connection closed by difusor
                print("Connection closed by difusor.")
                stop_event.set()
                break
            # Deserialize the message
            message = pickle.loads(data)
            if isinstance(message, Message):
                print(f"Received message: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")
            else:
                print("Received unknown data.")
        except Exception as e:
            print(f"Error receiving data: {e}")
            stop_event.set()
            break

def user_input_thread(sock, stop_event, quit_event):
    """Thread function to wait for user input to change type or exit."""
    while not stop_event.is_set():
        print("\nEnter 'c' to change type, 'q' to quit:")
        user_input = input().strip()
        if user_input.lower() == 'c':
            try:
                # Prompt for new desired type
                desired_type = int(input("Enter the new desired type of information (1-6): ").strip())
                if desired_type < 1 or desired_type > 6:
                    print("Invalid type. Please enter a number between 1 and 6.")
                    continue
                desired_types = [desired_type]
                control_message = ControlMessage(command='change_type', data=desired_types)
                sock.sendall(pickle.dumps(control_message))
                print(f"Requested to change type to {desired_type}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"Failed to send change type request to difusor: {e}")
                stop_event.set()
                break
        elif user_input.lower() == 'q':
            stop_event.set()
            quit_event.set()
            print("Exiting client.")
            break
        else:
            print("Invalid input. Please enter 'c' or 'q'.")

def main():
    while True:
        stop_event.clear()
        quit_event.clear()
        # Prompt the user for the desired type
        try:
            desired_type = int(input("Enter the desired type of information (1-6): ").strip())
            if desired_type < 1 or desired_type > 6:
                print("Invalid type. Please enter a number between 1 and 6.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        # Create a TCP connection to the difusor
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print(f"Connected to difusor at {HOST}:{PORT}")
        except Exception as e:
            print(f"Failed to connect to difusor: {e}")
            return

        # Send the desired type to the difusor
        try:
            desired_types = [desired_type]  # The difusor expects a list of types
            sock.sendall(pickle.dumps(desired_types))
            print(f"Requested type {desired_type} from difusor.")
        except Exception as e:
            print(f"Failed to send desired type to difusor: {e}")
            sock.close()
            return

        # Start the thread to receive messages
        recv_thread = threading.Thread(target=receive_messages, args=(sock, stop_event))
        recv_thread.start()

        # Start the thread to handle user input
        input_thread = threading.Thread(target=user_input_thread, args=(sock, stop_event, quit_event))
        input_thread.start()

        # Wait for both threads to finish
        recv_thread.join()
        input_thread.join()

        # Close the socket connection
        sock.close()

        # Check if the user wants to change type or exit
        if quit_event.is_set():
            # User chose to quit
            break
        else:
            # User chose to change type
            continue

if __name__ == '__main__':
    main()

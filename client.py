import socket
import threading
import pickle
from message import Message, ControlMessage  # Certifique-se de que ControlMessage está definido

HOST = '127.0.0.1'  
PORT = 1683

def receive_messages(sock, stop_event, quit_event):
    """Thread function to receive messages from the distributor."""
    while not stop_event.is_set():
        try:
            data = sock.recv(4096)
            if not data:
                # Connection closed by distributor
                print("Conexão fechada pelo difusor.")
                stop_event.set()
                quit_event.set()
                break
            # Deserialize the message
            message = pickle.loads(data)
            if isinstance(message, Message):
                print(f"Mensagem recebida: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")
            else:
                print("Dados desconhecidos recebidos.")
        except ConnectionResetError:
            # Distributor forcibly closed the connection
            print("Conexão fechada pelo difusor.")
            stop_event.set()
            quit_event.set()
            break
        except Exception as e:
            print(f"Erro ao receber dados: {e}")
            stop_event.set()
            quit_event.set()
            break

def user_input_thread(sock, stop_event, quit_event):
    """Thread function to handle user input to change type or exit."""
    while not stop_event.is_set():
        print("\nDigite 'c' para mudar o tipo, 'q' para sair:")
        user_input = input().strip()
        if user_input.lower() == 'c':
            try:
                # Prompt for new desired type
                desired_type = int(input("Digite o novo tipo de informação desejado (1-6): ").strip())
                if desired_type < 1 or desired_type > 6:
                    print("Tipo inválido. Por favor, insira um número entre 1 e 6.")
                    continue
                desired_types = [desired_type]
                control_message = ControlMessage(command='change_type', data=desired_types)
                sock.sendall(pickle.dumps(control_message))
                print(f"Solicitado mudança para o tipo {desired_type}")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número válido.")
            except Exception as e:
                print(f"Falha ao enviar solicitação de mudança de tipo para o difusor: {e}")
                stop_event.set()
                quit_event.set()
                break
        elif user_input.lower() == 'q':
            stop_event.set()
            quit_event.set()
            print("Saindo do cliente.")
            break
        else:
            print("Entrada inválida. Por favor, digite 'c' ou 'q'.")

    print("Thread de entrada do usuário encerrada.")

def main():
    while True:
        stop_event = threading.Event()
        quit_event = threading.Event()
        # Prompt the user for the desired type
        try:
            desired_type = int(input("Digite o tipo de informação desejado (1-6): ").strip())
            if desired_type < 1 or desired_type > 6:
                print("Tipo inválido. Por favor, insira um número entre 1 e 6.")
                continue
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")
            continue

        # Create a TCP connection to the distributor
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
            print(f"Conectado ao difusor em {HOST}:{PORT}")
        except Exception as e:
            print(f"Falha ao conectar-se ao difusor: {e}")
            return

        # Send the desired type to the distributor
        try:
            desired_types = [desired_type]  # The distributor expects a list of types
            sock.sendall(pickle.dumps(desired_types))
            print(f"Tipo {desired_type} solicitado ao difusor.")
        except Exception as e:
            print(f"Falha ao enviar o tipo desejado para o difusor: {e}")
            sock.close()
            return

        # Start the thread to receive messages
        recv_thread = threading.Thread(target=receive_messages, args=(sock, stop_event, quit_event))
        recv_thread.start()

        input_thread = threading.Thread(target=user_input_thread, args=(sock, stop_event, quit_event))
        input_thread.daemon = True  # This allows the program to exit even if input() is waiting
        input_thread.start()

        recv_thread.join()
        sock.close()

        # Check if the client should exit
        if quit_event.is_set():
            break
        else:
            continue

    print("Cliente finalizado.")

if __name__ == '__main__':
    main()

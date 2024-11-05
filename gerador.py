import time
import pickle
import random
import socket
import threading
from queue import Queue
from message import Message

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
locker = threading.Lock()
SERVER = '127.0.0.1'
PORT = 1682
dest = (SERVER, PORT)

categories = {
    "esportes": 1,
    "novidades da internet": 2,
    "eletrônicos": 3,
    "política": 4,
    "negócios": 5,
    "viagens": 6
}

def create_rand_num(min_value, max_value) -> int:
    """Generates a random number between the provided minimum and maximum value."""
    return random.randint(min_value, max_value)

def send_udp_message(sock, message):
    """Sends a serialized UDP message to the destination address."""
    try:
        serialized_message = pickle.dumps(message)
        sock.sendto(serialized_message, dest)
        print(f"Mensagem enviada: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def gera_msg_tread(fila, seq, tipo, VALOR_MIN, VALOR_MAX, T_MIN, T_MAX):
    """Function to create the generator and send messages continuously."""
    counter = 0 
    while True:
        valor = create_rand_num(VALOR_MIN, VALOR_MAX)
        fila.put(Message(counter, tipo, valor))
        counter += 1
        time.sleep(random.uniform(T_MIN, T_MAX))

def conf_gerador(i, types=[1,2,3,4,5,6]):
    """Function to configure the generator thread."""
    fila = Queue()
    print('Novo Gerador')
    for t in types:
        tmin = create_rand_num(1,10)
        tmax = create_rand_num(1,10)
        tmin, tmax = sorted((tmin, tmax))
        vmax = create_rand_num(1,200)
        threading.Thread(target=gera_msg_tread, args=(fila, None, t, 1, vmax, tmin, tmax), daemon=True).start()
    while True:
        if not fila.empty():
            locker.acquire()
            message = fila.get()
            info = pickle.dumps(message)
            udp.sendto(info, dest)
            locker.release()
        else:
            time.sleep(0.1)

def main():
    while True:
        try:
            num_geradores = int(input("Informe a quantidade de geradores a serem criados: "))
            if 0 <= num_geradores <= 6:
                break
            else:
                print("Por favor, insira um número entre 0 e 6.")
        except ValueError:
            print("Por favor, insira um número válido.")

    for i in range(num_geradores):
        print(f'Gerando os tipos do gerador {i+1}:')
        qtd_aleatoria = create_rand_num(1, 6)
        types_aleatorios = random.sample(list(categories.keys()), qtd_aleatoria)
        print(types_aleatorios)
        types = [categories[tipo] for tipo in types_aleatorios]

        threading.Thread(target=conf_gerador, args=(i, types), daemon=True).start()

    input("Pressione enter para encerrar!")
    print("Encerrando o programa...")

if __name__ == "__main__":
    main()

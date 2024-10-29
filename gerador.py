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

categorias = {
    "esportes": 1,
    "novidades da internet": 2,
    "eletrônicos": 3,
    "política": 4,
    "negócios": 5,
    "viagens": 6
}

def create_rand_num(min_value, max_value) -> int:
    """Gera um número aleatório entre o valor mínimo e máximo fornecido."""
    return random.randint(min_value, max_value)

def send_udp_message(sock, message):
    """Envia uma mensagem serializada UDP para o endereço destino."""
    try:
        serialized_message = pickle.dumps(message)
        sock.sendto(serialized_message, dest)
        print(f"Sent message: {message.seq}, {message.tipo}, {message.valor}")
    except Exception as e:
        print(f"Error sending message: {e}")

def gera_msg_tread(fila, seq, tipo, VALOR_MIN, VALOR_MAX, T_MIN, T_MAX):
    """Function to create the generator and send messages continuously."""
    counter = 0 
    while True:
        valor = create_rand_num(VALOR_MIN, VALOR_MAX)
        fila.put(Message(counter, tipo, valor))
        counter += 1
        time.sleep(random.uniform(T_MIN, T_MAX))

def conf_gerador(i, tipos=[1,2,3,4,5,6]):
    """Function to configure the generator thread."""
    fila = Queue()
    print('New Gerador')
    for t in tipos:
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
            break 
        except ValueError:
            print("Por favor, insira um número válido.")

    for i in range(num_geradores):
        print(f'Gerando os tipos dos geradores:')
        print(f'Ou pressione Enter para gerar todos os valores aleatórios.')

        qtd_aleatoria = create_rand_num(1, 6)
        tipos_aleatorios = random.sample(list(categorias.keys()), qtd_aleatoria)
        print(tipos_aleatorios)
        tipos = [categorias[tipo] for tipo in tipos_aleatorios]

        threading.Thread(target=conf_gerador, args=(i, tipos), daemon=True).start()

    input("Pressione enter para encerrar!")
    print("Encerrando o programa...")

if __name__ == "__main__":
    main()

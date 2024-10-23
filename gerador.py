import time
import pickle
import random
import socket
import threading
import gerador

SERVER = '127.0.0.1'
PORT = 1682
dest = (SERVER, PORT)

class Message:
    def __init__(self, seq, tipo, valor):
        self.seq = seq
        self.tipo = tipo
        self.valor = valor

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
        

def gerador_thread(seq, tipos):
    """Função para rodar o gerador e enviar mensagens continuamente."""
    gerador_instance = gerador.Gerador(
        sport="sport" in tipos, 
        news="news" in tipos, 
        eletronic="eletronic" in tipos, 
        policy="policy" in tipos, 
        business="business" in tipos, 
        travel="travel" in tipos
    )
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        tipo = random.choice(tipos)
        valor = create_rand_num(100, 1000)
        message = Message(seq, tipo, valor)
        send_udp_message(sock, message)
        seq += 1
        time.sleep(5)

def main():
    num_geradores = int(input("Informe a quantidade de geradores a serem criados: "))

    threads = []

    for i in range(num_geradores):

        tipos = input(f"Informe os tipos para o Gerador {i+1} separados por vírgula (ex: sport,news,travel): ").split(',')
        tipos = [tipo.strip() for tipo in tipos]
        

        thread = threading.Thread(target=gerador_thread, args=(i, tipos))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

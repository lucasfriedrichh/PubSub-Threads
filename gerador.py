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
        

def gera_info_tread(seq, tipo, VALOR_MAX, VALOR_MIN, T_MAX, T_MIN):
    """Função para criar o gerador e enviar mensagens continuamente."""
    
    
    


def conf_gerador(i, tipos = [1,2,3,4,5,6]):
    print('New Gerador')
        
    for t in tipos:
        tmin = create_rand_num(1,10)
        tmax = create_rand_num(1,10)
        vmax = create_rand_num(1,200)
        threading.Thread(target=gera_info_tread, args=(None, t, vmax, tmax, tmin))

            
    

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
        tipos = [categorias[tipo] for tipo in tipos_aleatorios]
            
        threading.Thread(target=conf_gerador, args=(i, tipos))


        


        
        
        
        
if __name__ == "__main__":
    main()

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
    """Gera um número aleatório entre o mínimo e o máximo fornecidos."""
    return random.randint(min_value, max_value)

def send_udp_message(sock, message):
    """Envia uma mensagem UDP serializada para o endereço de destino."""
    try:
        serialized_message = pickle.dumps(message)
        sock.sendto(serialized_message, dest)
        print(f"Mensagem enviada: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def gera_msg_tread(fila, seq, tipo, VALOR_MIN, VALOR_MAX, T_MIN, T_MAX, stop_event):
    """Função para criar o gerador e enviar mensagens continuamente."""
    counter = 0 
    while not stop_event.is_set():
        valor = create_rand_num(VALOR_MIN, VALOR_MAX)
        fila.put(Message(counter, tipo, valor))
        counter += 1
        time.sleep(random.uniform(T_MIN, T_MAX))

def conf_gerador(i, types=[1,2,3,4,5,6], stop_event=None):
    """Função para configurar a thread do gerador."""
    fila = Queue()
    print('Novo Gerador')
    for t in types:
        tmin = create_rand_num(1,10)
        tmax = create_rand_num(1,10)
        tmin, tmax = sorted((tmin, tmax))
        vmax = create_rand_num(1,200)
        threading.Thread(target=gera_msg_tread, args=(fila, None, t, 1, vmax, tmin, tmax, stop_event), daemon=True).start()
    while not stop_event.is_set():
        if not fila.empty():
            locker.acquire()
            message = fila.get()
            info = pickle.dumps(message)
            udp.sendto(info, dest)
            locker.release()
        else:
            time.sleep(0.1)

def main():
    generator_threads = []
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

        stop_event = threading.Event()
        t = threading.Thread(target=conf_gerador, args=(i, types, stop_event), daemon=True)
        t.start()
        generator_threads.append({'thread': t, 'stop_event': stop_event, 'id': i+1})

    while True:
        user_input = input("Pressione Enter para excluir um gerador ou digite 'sair' para encerrar: ")
        if user_input.lower() == 'sair':
            break
        else:
            if len(generator_threads) == 0:
                print("Não há geradores ativos.")
                continue
            elif len(generator_threads) == 1:
                # Se houver apenas um gerador, finalizar o programa
                print("Apenas um gerador restante. Encerrando o programa...")
                gen_to_stop = generator_threads[0]
                gen_to_stop['stop_event'].set()
                generator_threads.pop(0)
                break
            else:
                print("Geradores ativos:")
                for idx, gen in enumerate(generator_threads):
                    print(f"{idx+1}: Gerador {gen['id']}")
                choice = input("Informe o número do gerador a ser excluído ou 'sair' para encerrar: ")
                if choice.lower() == 'sair':
                    break
                elif choice == '':
                    continue  # Se o usuário apenas pressionar Enter, voltar ao início
                try:
                    num = int(choice)
                    if 1 <= num <= len(generator_threads):
                        gen_to_stop = generator_threads[num-1]
                        gen_to_stop['stop_event'].set()
                        print(f"Gerador {gen_to_stop['id']} excluído.")
                        generator_threads.pop(num-1)
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Por favor, insira um número válido.")

    # Encerrar todos os geradores restantes
    for gen in generator_threads:
        gen['stop_event'].set()
    print("Encerrando o programa...")

if __name__ == "__main__":
    main()

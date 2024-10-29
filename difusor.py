import time
import pickle
import socket

class Message:
    def __init__(self, seq, tipo, valor):
        self.seq = seq 
        self.tipo = tipo
        self.valor = valor

HOST = ''
PORT = 1682

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)
udp.bind(orig)




def main():
    seq_numbers = {}

    while True:
        print('\nWaiting for the message ...')
        msg_bytes, client = udp.recvfrom(1024)
        try:
            
            message = pickle.loads(msg_bytes)
            tipo = message.tipo
            seq = seq_numbers.get(tipo, 0) + 1
            seq_numbers[tipo] = seq
            message.seq = seq
            print(f"Received message from {client}")
            print(f"Message: seq={message.seq}, tipo={message.tipo}, valor={message.valor}")
        except Exception as e:
            print(f"An error occurred while processing the message: {e}")
            continue

        if isinstance(message.valor, str) and message.valor.lower() == 'end':
            print('Finalizing difusor')
            break

    udp.close()

if __name__ == '__main__':
    main()

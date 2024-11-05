# {TDE - Sockets e Threads - Pub Sub}

Projeto desenvolvido utilizando Python, com a biblioteca Threading.

Configurações de Ambiente:
SO: Ubuntu 24.04 
Python 3.11

## Pré-requisitos

Antes de começar, verifique se você possui as seguintes ferramentas instaladas em sua máquina:

- Node.js (versão 12 ou superior)
- npm (gerenciador de pacotes do Node.js)

## Passo 1: Clonar o repositório

Comece clonando este repositório para sua máquina local. Abra o terminal e execute o seguinte comando:

```bash
git clone https://github.com/lucasfriedrichh/PubSub-Threads.git
```

Isso criará uma cópia local do repositório em seu ambiente.


## Passo 2: Garantir que está com Python instalado
```bash
python3 --version
```

## Passo 3: Iniciar o programa
1. Podemos iniciar abrindo um novo terminal e executando o "gerador.py", na qual irá iniciar a gerar notícias sobre assuntos aleatórios.

```bash
python3 gerador.py
```

Assim que executarmos será criado a quantidade escolhida de geradores:
![image](https://github.com/user-attachments/assets/b7731ece-0bf3-4db8-8017-af1127d2c6f4)
Dessa forma, já temos os geradores criando as notícias.

2. Assim que os geradores forem iniciados, podemos executar o difusor, que vai fazer a intermediação e enviar as menssagens para cada 

```bash
python3 difusor.py
```

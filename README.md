# TDE - Sockets e Threads - Pub Sub

### Lucas Friedrich - 168238
### Leonardo Salinet - 179770


Projeto desenvolvido utilizando Python, com a biblioteca Threading.

## Ambiente de desenvolvimento e ferramentas
- SO: Ubuntu 24.04 
- Python 3.11

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
![image](https://github.com/user-attachments/assets/938b19b9-f823-4658-8c08-6c8bc7a6987d)

Dessa forma, já temos os geradores criando as notícias.

2. Assim que os geradores forem iniciados, podemos executar o difusor, que vai fazer a intermediação entre cliente as menssagens enviar as menssagens para cada cliente com seu respectivo assunto 

```bash
python3 difusor.py
```
![image](https://github.com/user-attachments/assets/23925d3a-fd2f-4730-8949-b99391d29f92)



2. Assim que os geradores forem iniciados, podemos executar o difusor, que vai fazer a intermediação e enviar as menssagens para cada cliente com seu respectivo assunto.
```bash
python3 cliente.py
```

![image](https://github.com/user-attachments/assets/ac3b0074-3f0b-4ba1-8c7e-5282acbc8416)



2. Assim que os geradores forem iniciados, podemos executar o difusor, que vai fazer a intermediação e enviar as menssagens para cada cliente com seu respectivo assunto 

![image](https://github.com/user-attachments/assets/96cc2728-21c3-4404-b724-2a016752b65c)



![image](https://github.com/user-attachments/assets/59699b13-fb20-4f82-bd93-0c1fe0cae571)



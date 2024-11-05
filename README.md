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

![1- gerador Init](https://github.com/user-attachments/assets/ceee2981-e24b-4957-a7eb-3c746e39c141)

Dessa forma, já temos os geradores criando as notícias.

2. Assim que os geradores forem iniciados, podemos executar o difusor, que vai fazer a intermediação entre cliente as menssagens enviar as menssagens para cada cliente com seu respectivo assunto 

```bash
python3 difusor.py
```
![2 - Difusor Init](https://github.com/user-attachments/assets/de814f0d-17a6-4fd9-bace-fa25d8c51794)


3. Após iniciar o difusor, podemos começar a criar a quantidade desejada de Clientes, respeitando a regra de criar apenas um cliente por terminal.
Podemos escolher qual tipo de noticia vamos receber.
```bash
python3 cliente.py
```
![3 - Client init](https://github.com/user-attachments/assets/1a593adf-7255-47ab-8347-c5cb18114fa9)


4. Programa já está iniciado!

## Passo 4: Possibilidades no programa.

1. Alterar tipo de noticia do cliente
- Clicando 'c' no terminal do cliente, podemos trocar o tipo de informação:

![4 - Alteração de Tipo CLIENTE](https://github.com/user-attachments/assets/3d6ea7e1-1dcd-4134-8f54-196249dcf9a0)

- Assim como quando criamos um cliente novo, quando alteramos, recebemos uma mensagem do client no difusor:

![7 - Cliente troca de tipo - DIFUSOR](https://github.com/user-attachments/assets/abe9f29a-eb3d-4e5e-a7b5-a98e8195b554)

2. Finalizar Cliente. 
- Clicando 'q' no terminal do cliente, finalizar o cliente:

![5 - Cliente fecha conexao - DIFUSOR](https://github.com/user-attachments/assets/3c7f1a67-e9bb-4079-add9-eea17b42d7bc)

- Quando finalizamos o Cliente o difusor recebe uma mensagem.

![6 - fechando o cliente - CLIENTE](https://github.com/user-attachments/assets/621998d6-ef6b-4493-9da8-3946a191d500)

3. Finalizar Difusor
- Para finalizar o difusor podemos clicar "Enter" em qualquer momento no terminal.

![8 - Finalização difusor - DIFUSOR](https://github.com/user-attachments/assets/b74802d8-434e-494b-9a5e-0d9e9a0da41e)

- Quando o difusor é finalizad, o cliente automaticamente fecha a comunicação e também pode ser finalizado.

![9 - Finalização difusor - CLIENTE](https://github.com/user-attachments/assets/fc74c878-789e-4c63-81df-1f34e6b8ed27)

4. Da mesma forma que podemos finalizar o difusor, podemos finalizar um ou todos os gerados.
- Escolhendo qual gerador queremos excluir e parar de gerar noticias.

![image](https://github.com/user-attachments/assets/6b65b3e0-2aab-4493-a816-09a5a7ec0ac1)


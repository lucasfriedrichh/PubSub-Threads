class Message:
    """
    Classe Message, para envio entre geradores->difusor->clietes

    Attributes:
        seq: Sequencia da mensagem.
        valor: Valor da mensagem.
        tipo: Valor que indica qual o tipo da mensagem.
    """

    def __init__(self, seq, tipo, valor):
        self.seq = seq
        self.tipo = tipo
        self.valor = valor
        
        
class ControlMessage:
    def __init__(self, command, data=None):
        self.command = command
        self.data = data

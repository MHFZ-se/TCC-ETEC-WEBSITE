from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(150))
    telefone = db.Column(db.String(15))
    senha = db.Column(db.String(255))
    email =  db.Column(db.String(40))
    numero_de_serie = db.Column(db.Integer , nullable=True)
    rota_foto_perfil = db.Column(db.String(60), nullable=True)
    adm = db.Column(db.Boolean)
    
def __init__(self, nome, telefone, senha, email, numero_de_serie,rota_foto_perfil,adm):
    self.id = id
    self.nome = nome
    self.telefone = telefone
    self.senha = senha
    self.email = email
    self.numero_de_serie = numero_de_serie
    self.rota_foto_perfil = rota_foto_perfil
    self.adm = adm
    
class Sensor(db.Model):
    numero_de_serie = db.Column(db.Integer, primary_key = True)
    id = db.Column(db.String(150))

def __init__(self, id, numero_de_serie):
    self.numero_de_serie = numero_de_serie
    self.id = id
    
class Coleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer)
    numero_de_serie = db.Column(db.Integer, db.ForeignKey('sensor.numero_de_serie'))
    data = db.Column(db.DateTime)
    corA = db.Column(db.String(24))
    led_vermelho = db.Column(db.Integer)
    led_verde = db.Column(db.Integer)
    led_azul = db.Column(db.Integer)

def __init__(self, id_usuario, data, corA, led_vermelho, led_verde, led_azul):
    self.id  = id
    self.id_usuario  = id_usuario
    self.data = data
    self.corA = corA
    self.led_vermelho = led_vermelho
    self.led_verde = led_verde
    self.led_azul = led_azul
    
    
    
    #modelos para o chat de atendimento ao cliente
class Atendimento(db.Model):
    id_atendimento = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer)
    id_adm = db.Column(db.Integer)
    data_abertura = db.Column(db.DateTime)
    estado = db.Column(db.String(25))
    assunto = db.Column(db.String(50))
    
def __init__(self, id_atendimento, id_cliente, id_adm, data_abertura, estado, assunto):
    self.id_atendimento = id_atendimento
    self.id_cliente = id_cliente
    self.id_adm = id_adm
    self.id_adm = id_adm
    self.data_abertura = data_abertura
    self.estado = estado
    self.assunto = assunto

class Mensagens(db.Model):
    id_mensagem = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.String(500))
    data_hora = db.Column(db.DateTime)
    id_remetente = db.Column(db.Integer)
    adm = db.Column(db.Boolean)


def __init__(self, id_mensagem , mensagem , id_remetente , adm):
    self.id_mensagem = id_mensagem
    self.mensagem = mensagem
    self.id_remetente = id_remetente 
    self.adm = adm 
    
    
    #relatos de bub ou plroblemas
class Problemas(db.Model):
    id_problema = db.Column(db.Integer, primary_key=True)
    id_cliente_afetado = db.Column(db.Integer)
    tpo_problema = db.Column(db.String(50))
    mensagem = db.Column(db.String(250))


def __init__(self, id_problema, id_cliente_afetado, tpo_problema, mensagem):
    self.id_problema = id_problema
    self.id_cliente_afetado =id_cliente_afetado
    self.tpo_problema =tpo_problema
    self.mensagem =mensagem
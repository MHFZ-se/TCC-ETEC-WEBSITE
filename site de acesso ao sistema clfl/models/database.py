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
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10))
    corA = db.Column(db.String(24))
    led_vermelho = db.Column(db.Integer)
    led_verde =  db.Column(db.Integer)
    led_azul = db.Column(db.Integer)

def __init__(self, data, corA, led_vermelho, led_verde, led_azul):
    self.id  = id
    self.data = data
    self.corA = corA
    self.led_vermelho = led_vermelho
    self.led_verde = led_verde
    self.led_azul = led_azul
    

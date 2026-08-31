#arquivo principal da aplicação
#configurando oque será usado/recursos essenciais
from flask import Flask
app = Flask(__name__, template_folder = 'views')
from controllers import routes
from werkzeug.security import generate_password_hash

import pymysql

from models.database import db, Usuario, Sensor, Coleta
#from models.database import db

#informa o nome do database
DB_NAME = 'planetHealth'

app.config['DATABASE_NAME'] = DB_NAME

app.config['SQLALCHEMY_DATABASE_URI']= f'mysql://root@localhost/{DB_NAME}'
#chave de encriptação de senha
app.config['SECRET_KEY'] = 'meusagrado'
#define tempo de sessao
app.config['PERMANENT_SESSION_LIFETIME'] = 11800 

#chama as rotas do site
#costumava ficar aq mas cresceu dms daí deixamo em outro lugar
routes.init_app(app)

if __name__ == '__main__':
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 charset='utf8mb4',
                                 cursorclass = pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            print("O Banco de Dados foi criado com sucesso!")
    except Exception as error:
        print(f"Erro ao criar o Banco de Dados: {error}")
    finally:
        connection.close()
        
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()

        for numero in range(1, 51):
            sensor = Sensor.query.get(numero)

            if sensor is None:
                sensor = Sensor(numero_de_serie=numero, id=None)
                db.session.add(sensor)
                
        usuarios = [
            
                Usuario(nome = "Henri Muniz Fudali", telefone = "122465423", senha = generate_password_hash("12345678"), email = "Henri@gmail", adm = 1),
                Usuario(nome = "Caio Muniz Iha", telefone = "122465423", senha = generate_password_hash("12345678"), email = "Caio@gmail", adm = 1),
                Usuario(nome = "Breno Mathias de Souza", telefone = "122465423", senha = generate_password_hash("12345678"), email = "Breno@gmail", adm = 1),
                Usuario(nome = "Eduarido Miguel Pereira", telefone = "122465423", senha = generate_password_hash("12345678"), email = "Eduardo@gmail", adm = 1)
            ]
        for usuario in usuarios:
            existente = Usuario.query.filter_by(email=usuario.email).first()

            if existente is None:
                db.session.add(usuario)
        
        db.session.commit()
        
    app.run(debug=True)
    
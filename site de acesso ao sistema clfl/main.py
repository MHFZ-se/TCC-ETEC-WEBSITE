#configurando oque será usado/recursos essenciais
from flask import Flask
app = Flask(__name__, template_folder = 'views')
from controllers import routes

import pymysql

from models.database import db, Usuario, Sensor, Coleta
#from models.database import db


DB_NAME = 'planetHealth'
app.config['DATABASE_NAME'] = DB_NAME
app.config['SQLALCHEMY_DATABASE_URI']= f'mysql://root@localhost/{DB_NAME}'
app.config['SECRET_KEY'] = 'meusagrado'
app.config['PERMANENT_SESSION_LIFETIME'] = 11800 

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
        
    app.run(debug=True)
    
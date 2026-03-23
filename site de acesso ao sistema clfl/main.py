#configurando oque será usado/recursos essenciais
from flask import Flask
from config import *  #chama os atributos do config.py
app = Flask(__name__, template_folder = 'views')
from controllers import routes

#conecta com lista de paginas
routes.init_app(app)

#print(home, macho)

#print("Hello world")
if __name__ == '__main__':
     app.run(debug=True)
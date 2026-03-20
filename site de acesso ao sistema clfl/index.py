#configurando oque será usado/recursos essenciais
from flask import Flask, render_template
from config import * #chama os atributos do config.py
app = Flask(__name__, template_folder = umbiRota+'paginas')


#pagina inicial
@app.route('/')
def home():
    return render_template("index.html")


#print(home, macho)

#print("Hello world")
if __name__ == '__main__':
     app.run(debug=True)
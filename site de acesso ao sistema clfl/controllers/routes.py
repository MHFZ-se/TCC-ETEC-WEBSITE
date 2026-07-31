
from flask import render_template, request, redirect, url_for, flash,session 
from models.database import Usuario,db
from controllers.funcoes import comparar, compararSenha
from markupsafe import Markup

from werkzeug.security import generate_password_hash,check_password_hash


def init_app(app):

    @app.route('/')
    def home(): 
        return render_template("index.html")# leva ao login e cadastro
    
    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == "POST":

            dados_login = request.form.to_dict()
            email = dados_login['email']
            senha = dados_login['senha']
            listaEmails = Usuario.query.with_entities(Usuario.email).all()#cria uma lista com todos os emails do banco, a longo prazo isso pode dar o maior BO cara...

            if comparar(email, listaEmails):#verifica se o email existe na lisara, o retorno da função é o id do usuario q porta o email

                if compararSenha(comparar(email, listaEmails), senha):
                    nome = db.session.query(Usuario.nome).filter_by(id=comparar(email, listaEmails)).scalar()
                    return redirect(url_for('interface',id=comparar(email, listaEmails),nome=nome))
                else: return "A senha não é compativel com o email informado, por favor tente de novo"

            else: return "O email informado não existe no banco ou foi digitado errado, por favor tente de novo"

        return render_template('login.html')
    
    @app.route('/cadastro', methods=['GET','POST'])
    def cadastro():
        #if id:
            
        if request.method == "POST":
            dados_form = request.form.to_dict()
            novoUsuario = Usuario(
                nome=dados_form['nome'],
                telefone=dados_form['telefone'],
                senha=dados_form['senha'],
                email=dados_form['email']
            )
            db.session.add(novoUsuario)
            # Confirmando a operação no banco
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('cadastro.html')
        
    @app.route('/interface')#
    def interface():
        return render_template('interface.html')
    
    @app.route('/centro/informacoes')#leva a ultima analise e anteriores
    def centroInfo():
        return 'falso(placeholder)'
    
    # @app.route('/centro/informacoes/ultima')#leva a consulta da ultima
    # def ultima():
    #     return 'falso'
    
    @app.route('/centro/informacoes/anteriores')#leva a consulta da que for clicada
    def anteriores():
        return 'falso'
    
    @app.route('/centro/informacoes/consulta')
    def consulta():
        return 'Verdadeiros(placeholder)'
    
    
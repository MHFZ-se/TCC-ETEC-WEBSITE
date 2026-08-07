
from flask import render_template, request, redirect, url_for, flash, session 
from models.database import Usuario,db
from controllers.funcoes import *
from markupsafe import Markup

from werkzeug.security import generate_password_hash,check_password_hash


def init_app(app):

    @app.route('/')
    def home(): 
        return render_template("index.html")# leva ao login e cadastro
    
    
    
    
    
    #login com senha e email
    @app.route('/login', methods=['GET','POST'])
    def login():
        
        if request.method == "POST":

            
            email = request.form['email']
            senha = request.form['senha']
            usuario = Usuario.query.filter_by(email=email).first()#cria uma lista com todos os emails do banco, a longo prazo isso pode dar o maior BO cara...

            if usuario:#checa se o usuario existe no banco

                if check_password_hash(usuario.senha,senha):# o primeiro parametro é a senha hashada e o segundo a senha do form
                    
                    session['idLogado'] = usuario.id
                    session['nomeLogado'] = usuario.nome
                    session['emailLogado'] = usuario.email
                    
                    return redirect(url_for('interface'))
                
                else: return "A senha não é compativel com o email informado, por favor tente de novo"

            else: return "O email informado não existe no banco ou foi digitado errado, por favor tente de novo"

        return render_template('login.html')
    
    
    
    
    
    
    
    
    
    @app.route('/cadastro', methods=['GET','POST'])
    def cadastro():
        #if id:
            
        if request.method == "POST":
            dadosPreenchidos = request.form.to_dict()
            
            email = dadosPreenchidos['email']
            usuario = Usuario.query.filter_by(email=email).first()
            
            if usuario:#verificando se o usuario ja existe no banco
                msg = Markup("")
                flash(msg,'danger')
                return redirect(url_for('cadastro'))#caso ja tenha uma conta com o mesmo email
            
            #Se não existir ele é criado
            senha = dadosPreenchidos['senha']
            senhaCodificada = generate_password_hash(senha,method='scrypt')
            
            novoUsuario = Usuario(
                
                email = email,
                senha = senhaCodificada,
                nome = dadosPreenchidos['nome'],
                telefone = dadosPreenchidos['telefone']
            )
            
            
            db.session.add(novoUsuario)
            # Confirmando a operação no banco
            db.session.commit()
            
            msg = Markup("")
            flash(msg,'danger')#conta criada
            return redirect(url_for('home'))#caso de tudo certo
        
        
        return render_template('cadastro.html')#se o metodo não for post
        
        
        
    @app.route('/sobrenos')#
    def sobrenos():
            return render_template('sobrenos.html')
        
        
        
        
        
        
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
    
    
    @app.route('/sair')
    def sair():
        session.clear()
        return redirect(url_for('home')) 
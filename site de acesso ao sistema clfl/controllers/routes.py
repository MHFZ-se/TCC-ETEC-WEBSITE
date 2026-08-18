
from flask import render_template, request, redirect, url_for, flash, session 
from models.database import Usuario,Sensor,db
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
            senha2 = dadosPreenchidos['senha2']
            
            if senha != senha2:
                return "Ambas as senhas devem ser iguais"

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
    
      
    @app.route('/interface/vincularSensor', methods=['GET', 'POST','PUT'])
    def vincularSensor():

        if request.method == "POST":
            # vamo planejar direito, um usuario tem varios sensores, um sensor só tem um usuario pr motivos de segurança
            #ja que as consultas são vinculadas ao sensor e não ao usuario(pode mudar)
            #os sensores ja existem pois são pre fabricados portanto eles podem ja existir no banco
            #ou seja não da pra cadastrar um sensor que não existe(ainda)
            #todo sensor produzido consta no banco
            #petcebi que seria mais adequado chamar de ferramenta 
            #consegui criar,
            #o sensor só pode ser vinculado se não tiver nenhum id associao
            #os sensores vão de 1 a 50 um numero fora disso é falso

            dados_form = request.form.to_dict()
            numero_de_serie = int(dados_form['numero_de_serie'])


            # sensor_existente = Sensor.query.filter_by(
            #     numero_de_serie=numero_de_serie
            # ).first()

            if numero_de_serie < 1 or numero_de_serie > 51:
                return "não existe nenhum sensor com este codigo por favor insira um valido"

                
            sensor = Sensor.query.get(numero_de_serie)
            if sensor.id is not None: 
                return "O sensor informado já está no nome de um usuario, entre em contato pelo suporte ou tente de novo"
            
            sensor.id = str(session['idLogado'])

            db.session.commit()
            
            return redirect(url_for('interface'))

        return render_template('vincSensor.html')
    
    @app.route('/interface/verSensores', methods=['GET','POST'])
    def verSensores():
        #planejamento
        #eu vou fazer um objeto, array, dicionario... sei la ja esqueci
        #que contenha todos os sensores de um usuario
        #vou fazer isso com um for que ve quais sensores tem o mesmo id da sessão logada e ai eu adciono, seria bem facil com ia
        #mas eu quero me desafiar

        #salva a lista com todos os sensores
        sensores = Sensor.query.all()

        sensores_do_user = []

        for sensor in sensores:
            if sensor.id is not None:
                if int(sensor.id) == session['idLogado']:
                    sensores_do_user.append(sensor)
        
        print(sensores_do_user)

        return render_template('verSensores.html', sensores_do_user= sensores_do_user)

    @app.route('/interface/removerSensor', methods=['GET', 'POST'])
    def removerSensor():
        
        return render_template('removerSensor.html')

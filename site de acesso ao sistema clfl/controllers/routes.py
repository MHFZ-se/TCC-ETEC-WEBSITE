
from flask import render_template, request, redirect, url_for, flash, session 
from models.database import Usuario,Sensor,db
from controllers.funcoes import *
from markupsafe import Markup
from controllers.funcoes import quantidade_de_sensores

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
                telefone = dadosPreenchidos['telefone'],
                adm = False
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
        return render_template('interface.html', quantidade_de_sensores = quantidade_de_sensores(session['idLogado']))
    
    
    
    
    @app.route('/centro/informacoes', methods=['GET','POST'])#leva a ultima analise e anteriores
    def centroInfo():
        usuarios = Usuario.query.all()
        
        nome = []
        
        for usuario in usuarios:
            if usuario.id is not None:
                if int(usuario.id) == session['idLogado']:
                            nome.append(usuario)
                
        print(nome)
        
        return render_template('centroInfo.html', nome= nome)
    
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
        
        #print(sensores_do_user)

        return render_template('verSensores.html', sensores_do_user = sensores_do_user)




    @app.route('/interface/removerSensor', methods=['GET', 'POST'])

    @app.route('/interface/removerSensor/<int:numero_de_serie>')
    def removerSensor(numero_de_serie=None):


        if numero_de_serie:#depois de clicar no botão deletar
            
            sensor = Sensor.query.filter_by(numero_de_serie = numero_de_serie).first()
            sensor.id = None
            db.session.commit()

            return redirect(url_for('verSensores'))
        #primeira entrada    

        sensores = Sensor.query.all()
        sensores_do_user = []

        for sensor in sensores:
            if sensor.id is not None:

                if int(sensor.id) == session['idLogado']:

                    sensores_do_user.append(sensor)
        
        return render_template('removerSensor.html', sensores_do_user = sensores_do_user)





    @app.route('/centro/informacoes/editar', methods=['GET', 'POST'])
    def editarInfos():

        id = session['idLogado']
        usuario = Usuario.query.filter_by(id=id).first()

        if request.method == "POST":

            dadosSubtitutos = request.form

            nome = dadosSubtitutos['nome']
            email = dadosSubtitutos['email']
            telefone = dadosSubtitutos['telefone']
            senha = dadosSubtitutos['senha']
            senha2 = dadosSubtitutos['senha2']

            if  nome == None or email == None or telefone == None or senha == None or senha2 == None:
                return "Preencha todos os campos!!!"
            

            if senha != senha2: 
                return "Informe Duas senhas iguais"
            
            usuario.nome = nome
            usuario.email = email
            usuario.telefone = telefone
            
            if check_password_hash(usuario.senha,senha) and check_password_hash(usuario.senha,senha2):
                db.session.commit()
                return redirect(url_for('centroInfo'))
            
            usuario.senha = generate_password_hash(senha)
            db.session.commit()
            return redirect(url_for('centroInfo'))
            

        return render_template('editInfos.html', usuario = usuario)
    
    @app.route('/analises')
    def analises():
        
        # Criando variáveis para simular uma análise do sensor de cor
        data = "2026-08-01"
        corA = "Verde saudável"
        led_vermelho = 45
        led_verde = 180
        led_azul = 60

        analise = {
            "data": data,
            "corA": corA,
            "led_vermelho": led_vermelho,
            "led_verde": led_verde,
            "led_azul": led_azul
        }

        lista_analises = [
            {"data": "2026-08-01", "corA": "Verde saudável", "led_vermelho": 45, "led_verde": 180, "led_azul": 60},
            {"data": "2026-08-05", "corA": "Verde claro",    "led_vermelho": 70, "led_verde": 190, "led_azul": 80},
            {"data": "2026-08-10", "corA": "Amarelado",      "led_vermelho": 150, "led_verde": 160, "led_azul": 40},
            {"data": "2026-08-15", "corA": "Azulada",         "led_vermelho": 30, "led_verde": 80, "led_azul": 120},
            {"data": "2026-08-20", "corA": "Verde saudável", "led_vermelho": 48, "led_verde": 178, "led_azul": 62},
        ]
        return render_template('analises.html', analises=lista_analises)

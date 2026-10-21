
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from models.database import *
from controllers.funcoes import *
from markupsafe import Markup
from controllers.funcoes import quantidade_de_sensores
from sqlalchemy import func
import colorsys
import random
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename

import os
import uuid

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
            usuario = Usuario.query.filter_by(email=email).first()

            if usuario:
                if check_password_hash(usuario.senha, senha):
                    session['idLogado'] = usuario.id
                    session['nomeLogado'] = usuario.nome
                    session['emailLogado'] = usuario.email
                    
                    flash(f"Bem-vindo de volta, {usuario.nome}!", 'success')
                    return redirect(url_for('interface'))
                
                else:
                    flash("A senha informada está incorreta. Tente novamente.", 'danger')
                    return redirect(url_for('login'))

            else:
                flash("Não encontramos uma conta com este e-mail.", 'danger')
                return redirect(url_for('login'))

        return render_template('login.html')
    
    

    
    
    @app.route('/cadastro', methods=['GET','POST'])
    @app.route('/cadastro', methods=['GET','POST'])
    def cadastro():
        
        if request.method == "POST":
            dadosPreenchidos = request.form.to_dict()
            
            email = dadosPreenchidos['email']
            usuario = Usuario.query.filter_by(email=email).first()
            
            if usuario:
                msg = Markup("Este e-mail já está cadastrado. Faça o <a href='/login'>login</a>.")
                flash(msg, 'danger')
                return redirect(url_for('cadastro'))
            
            senha = dadosPreenchidos['senha']
            senha2 = dadosPreenchidos['senha2']
            
            if senha != senha2:
                flash("As senhas informadas não são iguais.", 'danger')
                return redirect(url_for('cadastro'))

            senhaCodificada = generate_password_hash(senha, method='scrypt')
            
            novoUsuario = Usuario(
                email = email,
                senha = senhaCodificada,
                nome = dadosPreenchidos['nome'],
                telefone = dadosPreenchidos['telefone'],
                adm = False
            )
            
            db.session.add(novoUsuario)
            db.session.commit()
            
            flash("Cadastro realizado com sucesso! Faça login para continuar.", 'success')
            return redirect(url_for('login'))
        
        return render_template('cadastro.html')
        
        
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
            codinome = dados_form['nome']


            # sensor_existente = Sensor.query.filter_by(
            #     numero_de_serie=numero_de_serie
            # ).first()

            if numero_de_serie < 1 or numero_de_serie > 51:
                return "não existe nenhum sensor com este codigo por favor insira um valido"

                
            sensor = Sensor.query.get(numero_de_serie)
            if sensor.id is not None: 
                return "O sensor informado já está no nome de um usuario, entre em contato pelo suporte ou tente de novo"
            
            sensor.id = str(session['idLogado'])
            sensor.codinome = codinome

            db.session.commit()
            
            return redirect(url_for('interface'))

        return render_template('vincSensor.html')
    
    @app.route('/interface/renSensor', methods=['GET','POST'])
    def renSensor():
        numero_de_serie = request.args.get('numero_de_serie', type=int)
        sensor = Sensor.query.filter_by(numero_de_serie = numero_de_serie).first()

        if sensor is None:
            flash("Sensor não encontrado.", "danger")
            return redirect(url_for('verSensores'))
        
        
        if request.method == 'POST':
            dados = request.form
            novoCodinome = dados['codinome']
            sensor.codinome = novoCodinome
            

            db.session.commit()
            return redirect(url_for('verSensores'))
        
        
        
        return render_template('renSensor.html', sensor=sensor)
    
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

        if numero_de_serie:
            sensor = Sensor.query.filter_by(numero_de_serie=numero_de_serie).first()
            sensor.id = None
            db.session.commit()

            flash("Sensor desvinculado com sucesso.", 'success')
            return redirect(url_for('verSensores'))
        
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
            

            if  nome == None or email == None or telefone == None:
                return "Preencha todos os campos!!!"
            

            
            
            usuario.nome = nome
            usuario.email = email
            usuario.telefone = telefone
            
            
            db.session.commit()
            return redirect(url_for('centroInfo'))
            

        return render_template('editInfos.html', usuario = usuario)

    @app.route('/analises')
    def analises():
        if 'idLogado' not in session:
            flash('Faça login para ver suas análises.', 'danger')
            return redirect(url_for('login'))

        coletas = Coleta.query.all()
        lista_analises = []

        for coleta in coletas:
            # Chama a função de análise agronômica baseada no RGB guardado
            resultado = analisar_cor(
                coleta.led_vermelho, coleta.led_verde, coleta.led_azul
            )

        # Atribui todos os campos retornados pela análise ao objeto
        coleta.tipo = resultado.get('tipo', 'Desconhecido')
        coleta.deficiencia = resultado.get('deficiencia', '--')
        coleta.nivel = resultado.get('nivel', 'Baixo')
        coleta.indice_saude = resultado.get('indice_saude', 0)
        coleta.tom_verde = resultado.get('tom_verde', '--')
        coleta.diagnostico = resultado.get('diagnostico', '--')
        coleta.solucao = resultado.get('solucao', '--')

        # Formata a cor RGB para o preview visual no card do histórico
        r = coleta.led_vermelho if coleta.led_vermelho is not None else 0
        g = coleta.led_verde if coleta.led_verde is not None else 0
        b = coleta.led_azul if coleta.led_azul is not None else 0
        coleta.cor_rgb = f"rgb({r}, {g}, {b})"

        lista_analises.append(coleta)

        return render_template('analises.html', analises=lista_analises)

    @app.route('/analises/adicionarNova')
    def analiseAdd():
        return render_template('addAnalise.html')
    






    @app.route('/analises/adicionarNova/manual', methods=['GET','POST'])
    def analiseAddManu():
        if request.method == "POST":
            coleta = Coleta(
                id_usuario = session['idLogado'],
                numero_de_serie = request.form['idSensor'],
                data = datetime.now(),
                corA = request.form['corA'],
                led_vermelho = request.form['led_vermelho'],
                led_verde = request.form['led_verde'],
                led_azul = request.form['led_azul']
            )
            db.session.add(coleta)
            db.session.commit()
            
            return redirect(url_for('analises'))
        return render_template('addAnaliseManual.html')








    @app.route('/detalhes-deficiencia/<tipo>')
    def detalhes_deficiencia(tipo=None):

        info = informacoes.get(tipo)

        if info is None:
            return "Resultado não encontrado", 404


        return render_template( 'detalhes_deficiencia.html', info=info )
    
    @app.route('/galeria', methods=['POST'])
    def galeria():

        FILE_TYPES = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'avif'}

        usuario = db.session.get(Usuario, session['idLogado'])

        if usuario is None:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('login'))


        file = request.files.get('file')

        if file is None or file.filename == '':
            flash('Selecione uma imagem.', 'danger')
            return redirect(url_for('centroInfo'))


        extensao = file.filename.rsplit('.', 1)[-1].lower()

        if extensao not in FILE_TYPES:
            flash(
                'Arquivo não permitido! Envie PNG, JPG, JPEG, GIF ou WEBP.', 'danger'
            )
            return redirect(url_for('centroInfo'))

        # Se já existir uma foto antiga, remove do disco
        if usuario.rota_foto_perfil:
            foto_antiga = os.path.join(
                app.config['UPLOAD_FOLDER'], usuario.rota_foto_perfil
            )

        if os.path.exists(foto_antiga):
            os.remove(foto_antiga)

        # ESTES COMANDOS AGORA FICAM FORA DO IF ACIMA (funcionam para qualquer usuário)
        novo_nome = secure_filename(f'{uuid.uuid4().hex}.{extensao}')

        caminho = os.path.join(app.config['UPLOAD_FOLDER'], novo_nome)

        # Salva a nova imagem
        file.save(caminho)


        usuario.rota_foto_perfil = novo_nome

        db.session.commit()

        flash('Foto de perfil atualizada com sucesso!', 'success')

        return redirect(url_for('centroInfo'))



    #rotas para problemas com
    @app.route('/atendimento')
    def atendimentoAoCliente():
        return render_template('atendimento_ao_cliente.html')
    
    @app.route('/atendimento/chat-atendente', methods= ['GET','POST'])
    #@app.route('/atendimento/chat-atendente')
    def atendimentoAoClienteChat(id_atendimento=None,novo_atendimento = None, enviarMensagem = None):#se o usuario clicou em abrir uma conversa ja existente
        atendimentos = []
        atendimentos = Atendimento.query.filter_by(id_cliente = session['idLogado']).order_by(Atendimento.data_abertura.asc()).all()
        mensagens = []
        mensagens = Mensagens.query.order_by(Mensagens.data_hora.asc()).all()
        id_atendimento = request.args.get('id_atendimento', type=int)
        novo_atendimento = request.args.get('novo_atendimento', type=int)
        

        if request.method == 'POST' and novo_atendimento != 2:
                print('passou pelo enviar mensagem')
                
                id_atendimento = request.form['id_naoatendimento'] 
                mensagem = request.form['textoMensagem']
                
                #tratamento pra ver se ta nulo
                if mensagem == 'bananinha' :
                    return 0
                

                novaMensagem = Mensagens(
                    mensagem = mensagem,
                    data_hora = datetime.now(),
                    id_remetente = session['idLogado'],
                    adm = False,
                    id_atendimento = id_atendimento
                )

                db.session.add(novaMensagem)
                db.session.commit()


                return redirect(url_for('atendimentoAoClienteChat',id_atendimento=id_atendimento))
        
        
        if novo_atendimento:
            
            if novo_atendimento == 1:
                print('chegou no 1')
                return render_template('chat.html', novo_atendimento = 1)
            
            #ao receber o form
            if novo_atendimento == 2:
                opcao = request.form['opcao']
                texto = request.form['problemaTexto']
                
                if opcao == '' and not texto.strip():
                    flash("Você deve preencher pelo menos um dos campos com uma opção valida", 'danger')
                    print("passou aq 6")   
                    return render_template('chat.html', novo_atendimento = 1)
                
                elif opcao:
                    adm = escolher_adm()
                    atendimento = Atendimento(
                        id_cliente = session['idLogado'],
                        id_adm = adm.id,
                        data_abertura = datetime.now(),
                        estado = "Aberto",
                        assunto = opcao
                    )
                                        
                    db.session.add(atendimento)
                    db.session.commit()    
                    print("passou aq 5")    
                    return redirect(url_for('atendimentoAoClienteChat', novo_atendimento = 3))
                else:
                    adm = escolher_adm()
                    atendimento = Atendimento(
                        id_cliente = session['idLogado'],
                        id_adm = adm.id,
                        data_abertura = datetime.now(),
                        estado = "Aberto",
                        assunto = texto
                    )
                                        
                    db.session.add(atendimento)
                    db.session.commit()                        
                    print("passou aq 4")   
                    return redirect(url_for('atendimentoAoClienteChat', novo_atendimento = 3))
        
                
            if novo_atendimento == 3:
                ultimoAtendimentoAberto = Atendimento.query.filter_by(id_cliente = session['idLogado'], estado='aberto').order_by(Atendimento.data_abertura.desc()).first()
                idUltimoAtendimento = ultimoAtendimentoAberto.id_atendimento
                mensagensConversa = []
                admSelecionado = Usuario.query.filter_by(id = ultimoAtendimentoAberto.id_adm ).first()
                
                for mensagem in mensagens:
                    if mensagem.id_atendimento == idUltimoAtendimento:
                        mensagensConversa.append(mensagem)
        

                
                print("passou aq 2")   #a rota passa as mensagens da conversa(para mostralas), os atendimentos(para a barra lateral) e o ultimo atendimento(para os dados da convers))
                return render_template ('chat.html', atendimentos = atendimentos, mensagensConversa = mensagensConversa ,
                    esseAtendimento = ultimoAtendimentoAberto, admSelecionado =  admSelecionado)
  
        
         
        if id_atendimento:
            print("passou aq")
            mensagensConversa = []
            atendimento =  Atendimento.query.filter_by(id_atendimento = id_atendimento).first()
            admSelecionado = Usuario.query.filter_by(id = atendimento.id_adm).first()    

            for mensagem in mensagens:
                if mensagem.id_atendimento == id_atendimento:
                    mensagensConversa.append(mensagem)
                  
            
            return render_template('chat.html', atendimentos = atendimentos, mensagensConversa = mensagensConversa,
                            esseAtendimento = atendimento, admSelecionado = admSelecionado)
            
        #     return render_template('chat.html', atendimentos = atendimentos, mensagens = mensagens, id_conversa = id_atendimento)
            
       
        return render_template('chat.html', atendimentos = atendimentos)
    

    
    @app.route('/atendimento/feedback', methods=['GET', 'POST'])
    def feedback():
        if request.method == 'POST':
            dados = request.form

            rota_foto = None

            # if 'file' in request.files:
            #     arquivo = request.files['file']

            #     if arquivo.filename != '':
            #         rota_foto = arquivo.filename

            problema = Problemas(

                id_cliente_afetado=session['idLogado'],
                tipo_problema=dados['tipo'],
                mensagem=dados['msg_feedback'],
                rota_foto=rota_foto
            )

            db.session.add(problema)
            db.session.commit()

            flash("Feedback enviado com sucesso, muito obrigado pelo seu tempo😘.", 'success' )

            return redirect(url_for('atendimentoAoCliente'))


















        return render_template('feedback.html')
    










    
    @app.route('/centro/informacoes/editar/nova_senha', methods= ['GET','POST'])
    def novaSenha():
        id = session['idLogado']
        usuario = Usuario.query.filter_by(id=id).first()

        if request.method == "POST":

            dadosSubtitutos = request.form
            senhaAtual = dadosSubtitutos['senhaAtual']
            senha1 = dadosSubtitutos['novaSenha1']
            senha2 = dadosSubtitutos['novaSenha2']

            if senha1 != senha2: 
                flash("Preencha os campos de nova senha exatamente iguais",'danger')
                return render_template('novaSenha.html')
            
            if check_password_hash(usuario.senha, senhaAtual) is False:
                flash("Preencha o campo EXATAMENTE igual a sua senha atual",'danger')
                return render_template('novaSenha.html')
            
            usuario.senha = generate_password_hash(senha1)
            db.session.commit()
            return redirect(url_for('centroInfo'))
        return render_template('novaSenha.html')

    @app.route('/sensor')
    def pagina_sensor():
        """Página opcional do painel de monitoramento do sensor."""
        if 'idLogado' not in session:
            flash('Faça login para acessar o monitoramento.', 'warning')
            return redirect(url_for('login'))
        return render_template('sensor.html')

    @app.route('/api/dados-atuais', methods=['GET', 'POST'])
    def get_dados_esp():
        """Endpoint consumido pelo JavaScript do dashboard em tempo real."""
        global dados_atuais_memoria
        return jsonify(dados_atuais_memoria)

    @app.route('/dados', methods=['POST'])
    def receber_dados_esp():
        """Endpoint chamado via HTTP POST pelo ESP32."""
        global dados_atuais_memoria

        conteudo = request.get_json(silent=True)
        if not conteudo:
            return jsonify({'erro': 'JSON invalido ou ausente'}), 400

        r = conteudo.get('vermelho', 0)
        g = conteudo.get('verde', 0)
        b = conteudo.get('azul', 0)

        # Processamento agronômico avançado (HSV + ExG)
        r_norm = r / 255.0
        g_norm = g / 255.0
        b_norm = b / 255.0

        h, s, v = colorsys.rgb_to_hsv(r_norm, g_norm, b_norm)
        hue_graus = h * 360.0
        exg = (2 * g_norm) - r_norm - b_norm

        if (80 <= hue_graus <= 140) or (exg > 0.05 and g > r):
            tom = f'Verde Intenso ({round(hue_graus, 1)}°)'
            indice = round(min(100.0, max(70.0, (g_norm * 100) + (exg * 20))), 1)
            diag = 'Folha saudável com alta densidade de clorofila.'
            nutriente = 'Nenhum (Níveis de NPK equilibrados)'
            solucao = 'Manter o plano de rega e a adubação de manutenção vigentes.'
            nome_cor_banco = 'Verde claro saudavel'

        elif 50 <= hue_graus < 80:
            tom = f'Verde-Claro / Amarelado ({round(hue_graus, 1)}°)'
            indice = round(max(35.0, (hue_graus / 80.0) * 65.0), 1)
            diag = 'Clorose foliar detectada (Início de amarelamento).'
            nutriente = 'Nitrogênio (N) - Carência no desenvolvimento'
            solucao = 'Aplicar adubação rica em Nitrogênio (ex: Ureia).'
            nome_cor_banco = 'Verde claro'

        elif 30 <= hue_graus < 50:
            tom = f'Amarelo / Clorótico ({round(hue_graus, 1)}°)'
            indice = round(max(20.0, (hue_graus / 50.0) * 35.0), 1)
            diag = 'Clorose severa / Falta de pigmentação.'
            nutriente = 'Magnésio (Mg) ou Ferro (Fe)'
            solucao = 'Realizar pulverização foliar com Sulfato de Magnésio ou Quelato de Ferro.'
            nome_cor_banco = 'Amarelado'

        elif r > g and r > b:
            tom = 'Tons Amarronzados / Seco'
            indice = 15.0
            diag = 'Tecido foliar seco ou necrosado.'
            nutriente = 'Fósforo (P) ou Estresse Hídrico'
            solucao = 'Ajustar irrigação e aplicar adubo rico em Fósforo (ex: MAP).'
            nome_cor_banco = 'Necrose / Seca'

        else:
            tom = 'Indeterminado / Escuro'
            indice = 40.0
            diag = 'Iluminação insuficiente no sensor.'
            nutriente = 'Acompanhamento recomendado'
            solucao = 'Aproxime o sensor da folha.'
            nome_cor_banco = 'Indeterminado'

        # Atualiza a memória corretamente com os dados reais calculados
        horario_atual = datetime.now().strftime('%H:%M:%S')
        dados_atuais_memoria = {
            'vermelho': r,
            'verde': g,
            'azul': b,
            'indice_saude': indice,
            'tom_verde': tom,
            'diagnostico': diag,
            'deficiencia': nutriente,
            'solucao': solucao,
            'horario': horario_atual,
        }

        # Salva automaticamente a leitura na tabela Coleta do MySQL
        try:
            id_user = session.get('idLogado', 1)
            nova_coleta = Coleta(
                id_usuario=id_user,
                data=datetime.now().strftime('%Y-%m-%d'),
                corA=nome_cor_banco,
                led_vermelho=r,
                led_verde=g,
                led_azul=b,
            )
            db.session.add(nova_coleta)
            db.session.commit()
        except Exception as e:
            print(f'Erro ao salvar coleta automática no banco: {e}')

        # Log de sucesso no terminal
        print(
            f'[{horario_atual}] ESP32 -> R:{r} G:{g} B:{b} | Tom: {tom} | Saúde: {indice}%'
        )
        
        return (
            jsonify({'status': 'sucesso', 'dados': dados_atuais_memoria}),
            200,
        )
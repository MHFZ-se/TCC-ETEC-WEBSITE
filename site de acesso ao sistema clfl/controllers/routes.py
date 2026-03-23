from config import *
from flask import render_template

def init_app(app):

    @app.route('/')
    def home(): 
        return render_template("index.html")# leva ao login e cadastro
    
    @app.route('/login')#leva ao centro
    def login():
        return "Login"
    
    @app.route('/cadastro')#leva ao centro
    def cadastro():
        return 'cadastro'
        
    @app.route('/centro')#
    def centro():
        return 'centro'
    
    @app.route('/centro/informacoes')#leva a ultima analise e anteriores
    def centroInfo():
        return 'falso'
    
    @app.route('/centro/informacoes/ultima')#leva a consulta da ultima
    def ultima():
        return 'falso'
    
    @app.route('/centro/informacoes/anteriores')#leva a consulta da que for clicada
    def anteriores():
        return 'falso'
    
    @app.route('/centro/informacoes/consulta')
    def consulta():
        return 'Verdadeiros'
    
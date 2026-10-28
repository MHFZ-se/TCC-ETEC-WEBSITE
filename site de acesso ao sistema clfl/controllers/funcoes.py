from models.database import Sensor,db,Usuario,Atendimento
from sqlalchemy import func
import random

# pra deixa o codigo mais limpo vô ta deixando umas func aqui, sepa eu organizo doreito e faço um arquivo pra cada tema, se sobrar tempo
#13/10 de 2026, não sobrou, vai fica assim msm

#numera a quantidade de sensores vínculados a um id especifico
def quantidade_de_sensores(id):
    sensores = Sensor.query.filter(Sensor.id == id).all()
    return len(sensores)

def analisar_cor(r, g, b):

        # Possível deficiência de Nitrogênio
        if r > 130 and g > 130 and b < 100:
            return {
                "tipo": "nitrogenio",
                "deficiencia": "Possível deficiência de Nitrogênio (N)",
                "nivel": "Atenção"
            }

        # Possível deficiência de Fósforo
        elif r < 80 and g < 120 and b > 80:
            return {
                "tipo": "fosforo",
                "deficiencia": "Possível deficiência de Fósforo (P)",
                "nivel": "Atenção"
            }

        # Planta aparentemente saudável
        elif g > r and g > b:
            return {
                "tipo": "normal",
                "deficiencia": "Nenhuma deficiência aparente",
                "nivel": "Normal"
            }

        # Não foi possível identificar
        else:
            return {
                "tipo": "inconclusivo",
                "deficiencia": "Resultado inconclusivo",
                "nivel": "Inconclusivo"
            }
    
informacoes = {

            "nitrogenio": {

                "titulo": "Possível deficiência de Nitrogênio (N)",

                "descricao":
                "O nitrogênio é importante para o crescimento "
                "da planta e para a formação de clorofila.",

                "sintomas":
                "O amarelecimento das folhas, principalmente "
                "das folhas mais velhas, pode estar associado "
                "à deficiência de nitrogênio.",

                "manejo":
                "Verifique a disponibilidade de nitrogênio no solo "
                "e faça a correção da adubação de acordo com a "
                "necessidade da planta.",

                "confirmacao":
                "A cor da folha não confirma sozinha a deficiência. "
                "Realize uma nova análise e, quando possível, "
                "uma análise do solo."
            },


            "fosforo": {

                "titulo": "Possível deficiência de Fósforo (P)",

                "descricao":
                "O fósforo participa de processos importantes "
                "relacionados ao crescimento da planta.",

                "sintomas":
                "Algumas plantas podem apresentar folhas "
                "verde-escuras e coloração arroxeada ou "
                "avermelhada.",

                "manejo":
                "Verifique a disponibilidade de fósforo no solo "
                "e faça a correção da adubação de acordo com "
                "a necessidade da planta.",

                "confirmacao":
                "A coloração é apenas uma indicação inicial. "
                "Uma nova análise e, quando possível, uma análise "
                "do solo ajudam a confirmar o problema."
            },


            "normal": {

                "titulo": "Planta aparentemente saudável",

                "descricao":
                "A coloração identificada pelo sensor está "
                "dentro do padrão definido para uma planta "
                "aparentemente saudável.",

                "sintomas":
                "Não foram identificadas alterações de cor "
                "associadas às deficiências analisadas.",

                "manejo":
                "Continue realizando o monitoramento periódico "
                "da planta.",

                "confirmacao":
                "Continue realizando novas análises para "
                "acompanhar a evolução da planta."
            },


            "inconclusivo": {

                "titulo": "Resultado inconclusivo",

                "descricao":
                "A leitura não apresentou características "
                "suficientes para indicar uma possível deficiência.",

                "sintomas":
                "A coloração detectada não se enquadrou "
                "nos padrões utilizados pelo sistema.",

                "manejo":
                "Realize uma nova leitura, mantendo condições "
                "semelhantes de iluminação e posicionamento "
                "do sensor.",

                "confirmacao":
                "O resultado deve ser confirmado com novas "
                "medições e, quando possível, outros métodos "
                "de avaliação."
            }
        }
def escolher_adm():
            adms = (
                db.session.query(
                    Usuario,func.count(Atendimento.id_atendimento).label('quantidade'))
                    .outerjoin(Atendimento,Atendimento.id_adm == Usuario.id).filter(Usuario.adm == True).group_by(Usuario.id).all()
            )

            menor_quantidade = min(
                quantidade for usuario, quantidade in adms
            )

            adms_disponiveis = [
                usuario
                for usuario, quantidade in adms
                if quantidade == menor_quantidade
            ]

            return random.choice(adms_disponiveis)

def tratamento(variavel):# caio aqui é para colocar os tratamentos de forma mais detalhada possivel, cozinhe!
      
      return 0
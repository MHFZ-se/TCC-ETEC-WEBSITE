from models.database import Sensor

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
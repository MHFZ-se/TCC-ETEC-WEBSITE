from models.database import Sensor

#numera a quantidade de sensores vínculados a um id especifico
def quantidade_de_sensores(id):
    sensores = Sensor.query.filter(Sensor.id == id).all()
    return len(sensores)

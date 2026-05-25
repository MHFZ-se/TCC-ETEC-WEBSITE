from models.database import Usuario,db
def comparar(valor, lista):

    for email in lista:
        if email[0] == valor:
            return db.session.query(Usuario.id).filter_by(email=valor).first()[0]

    return False
def compararSenha(idUsuario,valor):
    if valor == db.session.query(Usuario.senha).filter_by(id=idUsuario).first()[0]:
        return True
    return False
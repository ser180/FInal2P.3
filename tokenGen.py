import jwt

def createToken(datos: dict):
    token: str = jwt.encode(payload=datos, key='secretkey', algorithm='HS256')
    return token

def validateToken(token: str):
    try:
        return jwt.decode(token, key='secretkey', algorithms=['HS256'])
    except Exception as e:
        return None

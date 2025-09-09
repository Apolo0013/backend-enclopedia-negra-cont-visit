from flask import request, jsonify, make_response, Flask
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = '123mvfamlNRN"SQL-N@F-RUN"queryselector(.teupaifdp)"' 
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])


def GetNumeroVisitante():
    conteudo = 0
    with open('cont.txt', 'r', encoding='UTF-8') as file:
        conteudo = file.read()
    return conteudo


def AddContDate():
    conteudo = 0
    with open('cont.txt', 'r', encoding='UTF-8') as file:
        conteudo = file.read()
    conteudo = int(conteudo)
    conteudo += 1
    with open('cont.txt', 'w', encoding='UTF-8') as file:
        file.write(str(conteudo))


@app.route('/addvisita', methods=["GET"])
def AddContVisita():
    token_existente = request.cookies.get('token')
    # ele exisir
    if token_existente: 
        return {'sucesso': False}, 201
    try:
        token = jwt.encode({
            'visita': True,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
        },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        resposta = make_response(jsonify({
            'sucesso': True
            }))
        expires = datetime.now(timezone.utc) + timedelta(minutes=30)  
        resposta.set_cookie(
                'token',
                token,
                httponly=True,
                samesite="None",
                secure=True,
                max_age=1800,
                expires=expires 
            )
        #add +1 visita
        AddContDate()
        return resposta
    except Exception:
        return {'sucesso': False}, 401
    

@app.route('/getnumerovisitante', methods=["GET"])
def GetNumeroVisititante():
    try:
        conteudo = GetNumeroVisitante()
        return {'sucesso': True, 'numero_visitantes': conteudo}, 201
    except Exception as error:
        print(error)
        return {'sucesso': False}, 201


if __name__ == '__main__':
    app.run(debug=True)
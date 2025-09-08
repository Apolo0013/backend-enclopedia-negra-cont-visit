from flask import request, jsonify, make_response, Flask
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.config['SECRET_KEY'] = '123mvfamlNRN"SQL-N@F-RUN"queryselector(.teupaifdp)"' 
CORS(app, supports_credentials=True)


def AddContDate():
    conteudo = 0
    with open('cont.txt', 'r', encoding='UTF-8') as file:
        conteudo = file.read()
    conteudo = int(conteudo)
    conteudo += 1
    with open('cont.txt', 'w', encoding='UTF-8') as file:
        file.write(str(conteudo))
    #retornando o numero de visita
    return conteudo


@app.route('/addvisita', methods=["GET"])
def AddContVisita():
    token_existente = request.cookies.get('token')
    # ele exisir
    if (token_existente): 
        return {'sucesso': False}, 401
    try:
        token = jwt.encode({
            'visita': True,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
        },
            app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        numero_total_visitante = AddContDate()
        resposta = make_response(jsonify({
            'sucesso': True,
            'total_visitante': numero_total_visitante
            }))
        resposta.set_cookie(
                'token',
                token,
                httponly=True,
                samesite='Lax',
                secure=False,
                max_age=1800    
            )
        return resposta
    except Exception:
        return {'sucesso': False}, 401

if __name__ == '__main__':
    app.run(debug=True)
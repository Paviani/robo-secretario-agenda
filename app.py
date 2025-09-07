from flask import Flask, jsonify, request
from agendador import encontrar_horarios_disponiveis, marcar_consulta
from datetime import datetime, timedelta, timezone


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/encontrar_horarios")
def encontrar_horarios():

 # 1. Preparamos os "ingredientes" para a nossa função
    meus_calendarios = ['jarpaviani@gmail.com']
    agora = datetime.now(timezone.utc)
    inicio_busca = agora
    fim_busca = agora + timedelta(days=7)
    duracao_consulta = 50

    # 2. Chamamos a função com os ingredientes
    horarios_livres = encontrar_horarios_disponiveis(
        lista_ids_calendarios=meus_calendarios,
        data_inicio=inicio_busca,
        data_fim=fim_busca,
        duracao_minutos=duracao_consulta
    )

    # Primeiro, criamos uma nova lista convertendo cada objeto datetime para texto no padrão ISO
    horarios_em_texto = [horario.isoformat() for horario in horarios_livres]

    # Então, retornamos essa lista de textos no formato JSON, que é o padrão para APIs
    return jsonify(horarios_em_texto)

@app.route("/marcar_consulta", methods=["POST"])
def agendar_consulta():
    return None

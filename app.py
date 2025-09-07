from flask import Flask, jsonify, request
from agendador import encontrar_horarios_disponiveis, marcar_consulta
from datetime import datetime, timedelta, timezone

MEUS_CALENDARIOS = ['jarpaviani@gmail.com']
DURACAO_CONSULTA = 50 # Em minutos

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

    # 2. Chamar a função enccontrar_horários_disponiveis
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
    dados = request.get_json()
       
    nome = dados.get("nome_paciente")
    telefone = dados.get("telefone_paciente")
    horario_escolhido = dados.get("horario_escolhido")
    
    if not all([nome, telefone, horario_escolhido]):
        return jsonify({"status": "erro", "mensagem": "Dados faltando"}), 400
 
    #convertendo o texto do horário_escohido para um objeto datetime.
    data_hora_inicio = datetime.fromisoformat(horario_escolhido)
    
    #chamando a função marcar_consulta
    marcar_consulta(
        calendar_id= MEUS_CALENDARIOS[0], #usando a configuração global
        nome_paciente = nome,
        telefone_paciente = telefone,
        data_hora_inicio = data_hora_inicio,
        duracao_minutos = DURAÇÃO_CONSULTA #usando a configuração global
    )
    
    return jsonify({"status": "sucesso", "mensagem": "Consulta marcada com sucesso"})
    
    

    
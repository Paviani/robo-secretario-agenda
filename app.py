import os
from functools import wraps
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from agendador import encontrar_horarios_disponiveis, marcar_consulta
from datetime import datetime, timedelta, timezone

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações Carregadas do Ambiente ---
API_KEY = os.environ.get("API_KEY")
CALENDAR_ID = os.environ.get("CALENDAR_ID")
MEUS_CALENDARIOS = [CALENDAR_ID] if CALENDAR_ID else []
DURACAO_CONSULTA = 50 # Em minutos

app = Flask(__name__)

# --- Decorator para Autenticação ---
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-Key') and request.headers.get('X-API-Key') == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"status": "erro", "mensagem": "Chave de API inválida ou ausente"}), 401
    return decorated_function

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/encontrar_horarios")
@require_api_key
def encontrar_horarios():
    agora = datetime.now(timezone.utc)
    inicio_busca = agora
    fim_busca = agora + timedelta(days=7)

    horarios_livres = encontrar_horarios_disponiveis(
        lista_ids_calendarios=MEUS_CALENDARIOS,
        data_inicio=inicio_busca,
        data_fim=fim_busca,
        duracao_minutos=DURACAO_CONSULTA
    )

    horarios_em_texto = [horario.isoformat() for horario in horarios_livres]
    return jsonify(horarios_em_texto)

@app.route("/marcar_consulta", methods=["POST"])
@require_api_key
def agendar_consulta():
    dados = request.get_json()
       
    nome = dados.get("nome_paciente")
    telefone = dados.get("telefone_paciente")
    horario_escolhido = dados.get("horario_escolhido")
    
    if not all([nome, telefone, horario_escolhido]):
        return jsonify({"status": "erro", "mensagem": "Dados faltando"}), 400
 
    try:
        data_hora_inicio = datetime.fromisoformat(horario_escolhido)
    except (ValueError, TypeError):
        return jsonify({"status": "erro", "mensagem": "Formato de data inválido. Use o padrão ISO 8601."}), 400

    # Garante que o horário recebido tem informação de fuso horário
    if data_hora_inicio.tzinfo is None:
        return jsonify({"status": "erro", "mensagem": "O horário escolhido deve incluir informação de fuso horário (timezone)."}), 400

    marcar_consulta(
        calendar_id=MEUS_CALENDARIOS[0],
        nome_paciente=nome,
        telefone_paciente=telefone,
        data_hora_inicio=data_hora_inicio,
        duracao_minutos=DURACAO_CONSULTA
    )
    
    return jsonify({"status": "sucesso", "mensagem": "Consulta marcada com sucesso"})
    
    

    
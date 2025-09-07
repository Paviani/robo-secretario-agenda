import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone

# --- Autenticação ---

KEY_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = service_account.Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

# ---- Função para encontrar horários disponíveis --- #

def encontrar_horarios_disponiveis(lista_ids_calendarios, data_inicio, data_fim, duracao_minutos):
    """
    Encontra horários disponíveis em uma lista de agendas do Google Calendar.
    """
    # GARANTINDO QUE NOSSAS DATAS ESTÃO "CONSCIENTES" DO FUSO HORÁRIO UTC
    if data_inicio.tzinfo is None:
        data_inicio = data_inicio.astimezone(timezone.utc)
    if data_fim.tzinfo is None:
        data_fim = data_fim.astimezone(timezone.utc)

    # Montando a lista de agendas para a consulta
    items = [{"id": calendar_id} for calendar_id in lista_ids_calendarios]

    body = {
        "timeMin": data_inicio.isoformat(),
        "timeMax": data_fim.isoformat(),
        "timeZone": "UTC", # Especificando que queremos a resposta em UTC
        "items": items
    }

    # Faz a requisição para a API freebusy
    response = service.freebusy().query(body=body).execute()
    
    # Juntando todos os horários ocupados de todas as agendas em uma única lista
    todos_horarios_ocupados = []
    for calendar_id in lista_ids_calendarios:
        todos_horarios_ocupados.extend(response['calendars'][calendar_id]['busy'])

    # Ordenando os horários ocupados para facilitar a verificação
    todos_horarios_ocupados.sort(key=lambda x: x['start'])

    horarios_disponiveis = []
    # Começamos a procurar a partir do início do período
    ponteiro_tempo = data_inicio

    # Ordena os horários ocupados para processar em ordem
    todos_horarios_ocupados.sort(key=lambda x: datetime.fromisoformat(x['start'].replace('Z', '+00:00')))
    
    # Converte as strings da API para objetos datetime "conscientes" do UTC uma única vez
    eventos_ocupados = [
        (datetime.fromisoformat(o['start'].replace('Z', '+00:00')), datetime.fromisoformat(o['end'].replace('Z', '+00:00')))
        for o in todos_horarios_ocupados
    ]

    while ponteiro_tempo + timedelta(minutes=duracao_minutos) <= data_fim:
        slot_proposto_fim = ponteiro_tempo + timedelta(minutes=duracao_minutos)
        conflito = False

        for ocupado_inicio, ocupado_fim in eventos_ocupados:
            # Se o nosso slot terminar DEPOIS que um bloqueio começar
            # E o nosso slot começar ANTES que o mesmo bloqueio termine, há uma sobreposição
            if slot_proposto_fim > ocupado_inicio and ponteiro_tempo < ocupado_fim:
                # Conflito encontrado!
                conflito = True
                # Pula o ponteiro para o final do evento que causou o conflito
                ponteiro_tempo = ocupado_fim
                break # Sai do loop 'for' e vai para o próximo 'while' com o novo ponteiro
        
        if not conflito:
            # Se o loop 'for' terminou sem encontrar conflitos, o slot está livre
            horarios_disponiveis.append(ponteiro_tempo)
            # Avança o ponteiro por um intervalo mínimo para encontrar o próximo slot
            # (pode ser a duração ou um valor fixo como 15/30 min)
            ponteiro_tempo += timedelta(minutes=15) # Avança de 15 em 15 minutos para procurar o próximo
    
    return horarios_disponiveis

# --- Exemplo de uso ---
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    calendar_id = os.environ.get("CALENDAR_ID")
    if not calendar_id:
        raise ValueError("A variável de ambiente CALENDAR_ID não foi definida.")
    meus_calendarios = [calendar_id]
    
    # Definindo o período que queremos verificar (hoje e os próximos 7 dias)
    agora = datetime.now(timezone.utc)
    inicio_busca = agora
    fim_busca = agora + timedelta(days=7)

    # Chamando sua função para encontrar horários de 50 minutos
    horarios = encontrar_horarios_disponiveis(
        lista_ids_calendarios=meus_calendarios,
        data_inicio=inicio_busca,
        data_fim=fim_busca,
        duracao_minutos=50
    )

    print(f"Encontrados {len(horarios)} horários disponíveis de 50 minutos nos próximos 7 dias:")
    for horario in horarios:
        # Imprime o horário convertido para a hora local de São Paulo para facilitar a leitura
        print(horario.astimezone(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M'))

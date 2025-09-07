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

# Função para marcar consulta

def marcar_consulta(calendar_id, nome_paciente, telefone_paciente, data_hora_inicio, duracao_minutos):
        
        """
    Cria um evento na agenda do Google.

    Args:
        calendar_id (str): O ID da agenda onde o evento será criado.
        nome_paciente (str): O nome do paciente para o título.
        telefone_paciente (str): O telefone para a descrição.
        data_hora_inicio (datetime): O objeto datetime de quando o evento deve começar.
        duracao_minutos (int): A duração da consulta em minutos.
        """
        
        # 1. Calcular o horário de fim
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao_minutos)
        
        # 2. Definir os detalhes do evento usando os parâmetros da função
        event = {
        'summary': f'Consulta - {nome_paciente}', # Usando o nome do paciente no título
        'description': f'Telefone para contato: {telefone_paciente}', # E o telefone na descrição
        'start': {
            'dateTime': data_hora_inicio.isoformat(),
        },
        'end': {
            'dateTime': data_hora_fim.isoformat(),
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                #{'method': 'email', 'minutes': 24 * 60},  Lembrete por e-mail 24 horas antes (não pretendo usar agora)
                {'method': 'popup', 'minutes': 30},      # Lembrete pop-up 30 minutos antes
            ],
        },
}
        
        print(f"\nAgendando consulta para {nome_paciente} na agenda: {calendar_id}")
        
        # Executando a ordem para CRIAR (insert) o evento
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

        print("\nSUCESSO!")
        print(f"Evento criado: {created_event.get('summary')}")
        print(f"Veja o evento aqui: {created_event.get('htmlLink')}")
        
# --- Bloco Principal de Execução (Exemplo de uso) ---
if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    # --- 1. CONFIGURAÇÕES ---
    calendar_id = os.environ.get("CALENDAR_ID")
    if not calendar_id:
        raise ValueError("A variável de ambiente CALENDAR_ID não foi definida.")
    meus_calendarios = [calendar_id]
    duracao_consulta = 50
    
    # --- 2. ENCONTRAR HORÁRIOS DISPONÍVEIS ---
    print("Buscando horários disponíveis...")
    agora = datetime.now(timezone.utc)
    inicio_busca = agora
    fim_busca = agora + timedelta(days=7)

    horarios_livres = encontrar_horarios_disponiveis(
        lista_ids_calendarios=meus_calendarios,
        data_inicio=inicio_busca,
        data_fim=fim_busca,
        duracao_minutos=duracao_consulta
    )

    # --- 3. MARCAR A CONSULTA NO PRIMEIRO HORÁRIO LIVRE ---
    if horarios_livres:
        primeiro_horario = horarios_livres[0]
        fuso_horario_local = timezone(timedelta(hours=-3)) # Fuso de São Paulo
        
        print(f"\nHorário disponível encontrado: {primeiro_horario.astimezone(fuso_horario_local).strftime('%d/%m/%Y às %H:%M')}")
        
        # Usando o primeiro horário livre para agendar uma consulta de teste
        marcar_consulta(
            calendar_id=meus_calendarios[0],
            nome_paciente="Maria Exemplo",
            telefone_paciente="(11) 91234-5678",
            data_hora_inicio=primeiro_horario,
            duracao_minutos=duracao_consulta
        )
    else:
        print("\nNão foram encontrados horários disponíveis no período solicitado.")
        

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

# Este é o "endereço" da agenda onde o robô vai escrever.
calendar_id = 'jarpaviani@gmail.com' 

# Criação de teste para evento daqui a 5 minutos
now = datetime.now(timezone.utc)
start_time = now + timedelta(minutes=5)
end_time = start_time + timedelta(minutes=45) # Duração de 15 minutos

# Definindo os detalhes do evento
event = {
  'summary': 'Reunião de Alinhamento',
  'description': 'EDiscutir próximos passos do projeto Robô Secretário',
  'start': {
    'dateTime': start_time.isoformat(),  # O .isoformat() de um objeto 'aware' já contém o fuso horário
  },
  'end': {
    'dateTime': end_time.isoformat(), # O .isoformat() de um objeto 'aware' já contém o fuso horário
  },
}

print(f"Criando um evento de teste na agenda: {calendar_id}")

# Executando a ordem para CRIAR (insert) o evento
created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

print("\nSUCESSO!")
print(f"Evento criado: {created_event.get('summary')}")
print(f"Veja o evento aqui: {created_event.get('htmlLink')}")
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. O CAMINHO PARA A NOSSA CHAVE SECRETA
# Garante que o script encontre o arquivo credentials.json na mesma pasta que ele está.
KEY_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'credentials.json')

# 2. AS PERMISSÕES QUE ESTAMOS PEDINDO
# Estamos dizendo que nosso robô quer acesso de leitura e escrita nos calendários.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# 3. AUTENTICAÇÃO
# Cria as credenciais do nosso robô a partir do arquivo JSON.
creds = service_account.Credentials.from_service_account_file(
        KEY_FILE_LOCATION, scopes=SCOPES)

# 4. CONSTRUINDO O "CONTROLE REMOTO" DA API
# Cria um objeto 'service' que sabe como "conversar" com a API do Google Agenda.
service = build('calendar', 'v3', credentials=creds)

print("Conexão bem-sucedida! Buscando agendas...")

# 5. EXECUTANDO A PRIMEIRA AÇÃO
# Pede à API para listar todas as agendas na "lista de agendas" do nosso robô.
calendar_list = service.calendarList().list().execute()

print("Agendas que o robô tem acesso:")
# 6. MOSTRANDO O RESULTADO
# Itera sobre a resposta e imprime o 'summary' (o nome) de cada agenda encontrada.
for calendar_list_entry in calendar_list['items']:
    print(f"- {calendar_list_entry['summary']}")
import os
import pytest
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 1. O CAMINHO PARA A NOSSA CHAVE SECRETA
# Garante que o script encontre o arquivo credentials.json na mesma pasta que ele está.
KEY_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'credentials.json')

# 2. AS PERMISSÕES QUE ESTAMOS PEDINDO
# Estamos dizendo que nosso robô quer acesso de leitura e escrita nos calendários.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def test_conexao():
    """Verifica se a API do Google Agenda está acessível."""
    if not os.path.exists(KEY_FILE_LOCATION):
        pytest.skip("Arquivo de credenciais não encontrado.")

    try:
        creds = service_account.Credentials.from_service_account_file(
            KEY_FILE_LOCATION, scopes=SCOPES
        )
        service = build('calendar', 'v3', credentials=creds)

        # 5. EXECUTANDO A PRIMEIRA AÇÃO
        calendar_list = service.calendarList().list().execute()

        # 6. VERIFICANDO O RESULTADO
        assert calendar_list.get('items'), "Lista de agendas vazia."
    except Exception as e:
        pytest.fail(f"Falha na autenticação ou conexão: {e}")


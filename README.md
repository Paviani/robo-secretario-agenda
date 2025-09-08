# Robô Agendador para Google Calendar

Este projeto automatiza a gestão de agendas no Google Calendar. Ele pode ser executado como um conjunto de scripts de linha de comando ou como uma API Web, permitindo encontrar horários disponíveis e marcar novos eventos (consultas, reuniões, etc.).

## Segurança

Para garantir que apenas aplicações autorizadas possam usar esta API, o acesso aos endpoints é protegido por uma Chave de API (API Key). Todas as requisições devem incluir um cabeçalho `X-API-Key` contendo a chave secreta definida.

## Funcionalidades do Projeto

O projeto oferece duas formas de uso: scripts individuais ou uma API Web.

### Scripts de Linha de Comando

-   `agendador.py`: Script principal que busca por horários vagos e marca uma consulta de exemplo no primeiro horário encontrado.
-   `encontra-agenda.py`: Versão simplificada que apenas realiza a busca por horários disponíveis e os exibe no terminal.
-   `teste_conexao.py`: Script de diagnóstico para verificar a autenticação com a API do Google Calendar.
-   `teste_escrita.py`: Script de diagnóstico para verificar a permissão de escrita, tentando criar um evento de teste.

### API Web com Flask (`app.py`)

-   `app.py`: Uma aplicação web construída com Flask que expõe a funcionalidade de agendamento através de uma API RESTful. Ideal para integrar com outras aplicações ou front-ends.

## API Web com Flask

A API oferece endpoints para interagir com o agendador de forma programática.

### Endpoint: `GET /encontrar_horarios`

Busca por horários disponíveis na agenda configurada.

-   **Método:** `GET`
-   **Resposta de Sucesso (200 OK):** Um JSON contendo uma lista de horários disponíveis em formato de string [ISO 8601](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString).
    ```json
    [
      "2023-10-27T14:00:00+00:00",
      "2023-10-27T15:00:00+00:00",
      "2023-10-27T16:00:00+00:00"
    ]
    ```

### Endpoint: `POST /marcar_consulta`

Agenda uma nova consulta no horário escolhido.

-   **Método:** `POST`
-   **Corpo da Requisição (JSON):**
    ```json
    {
      "nome_paciente": "João da Silva",
      "telefone_paciente": "+5511999998888",
      "horario_escolhido": "2023-10-27T14:00:00+00:00"
    }
    ```
-   **Respostas:**
    -   **Sucesso (200 OK):**
        ```json
        {
          "status": "sucesso",
          "mensagem": "Consulta marcada com sucesso"
        }
        ```
    -   **Erro (400 Bad Request):**
        ```json
        {
          "status": "erro",
          "mensagem": "Dados faltando"
        }
        ```

## Configuração e Instalação

Para utilizar este projeto, você precisará de uma conta Google e um projeto no Google Cloud Platform.

### Pré-requisitos
- Python 3.6 ou superior.
- Uma conta do Google com o Google Calendar ativado.

### 1. Configuração do Projeto no Google Cloud

(As instruções para criar projeto, ativar API, criar Service Account e obter a chave JSON permanecem as mesmas)

1.  **Crie um novo projeto** no [Google Cloud Console](https://console.cloud.google.com/).
2.  **Ative a API do Google Calendar**.
3.  **Crie uma Conta de Serviço (Service Account)**.
4.  **Crie uma chave JSON** para a Conta de Serviço e renomeie-a para `credentials.json` na raiz do projeto.

### 2. Compartilhe sua Agenda

(As instruções para compartilhar a agenda com o e-mail da Service Account permanecem as mesmas)

Compartilhe sua agenda com o e-mail da conta de serviço, concedendo a permissão **"Fazer alterações nos eventos"**.

### 3. Crie seu arquivo de configuração

Renomeie o arquivo `.env.example` para `.env` e preencha as variáveis necessárias, como o `CALENDAR_ID` e a sua `API_KEY` secreta.

### 4. Instalação das Dependências

Este projeto utiliza um arquivo `requirements.txt` para gerenciar suas dependências. Instale-as usando `pip`:

```bash
pip install -r requirements.txt
```

## Como Usar

Depois de concluir a configuração, você pode executar os scripts ou a API Web.

### Opção 1: Executando os Scripts Individualmente

Para tarefas específicas ou testes, você pode executar os scripts diretamente.

-   **Verificar a Conexão:**
    ```bash
    python teste_conexao.py
    ```
-   **Verificar a Permissão de Escrita:**
    ```bash
    python teste_escrita.py
    ```
-   **Encontrar Horários Disponíveis:**
    ```bash
    python encontra-agenda.py
    ```
-   **Agendar uma Consulta (Exemplo):**
    ```bash
    python agendador.py
    ```

### Opção 2: Executando a API Web

Para expor a funcionalidade como um serviço, use o Flask.

1.  **Exporte a variável de ambiente `FLASK_APP`**:
    ```bash
    # No Linux/macOS
    export FLASK_APP=app.py

    # No Windows (cmd)
    set FLASK_APP=app.py
    ```

2.  **Inicie o servidor de desenvolvimento**:
    ```bash
    flask run
    ```

O servidor estará rodando em `http://127.0.0.1:5000`. Agora você pode fazer requisições para os endpoints `/encontrar_horarios` e `/marcar_consulta` usando ferramentas como `curl` ou Postman.

### Configurando o Agendador

Tanto os scripts quanto a API utilizam as seguintes variáveis globais definidas no topo dos arquivos `agendador.py` e `app.py`:

-   `MEUS_CALENDARIOS`: Uma lista de IDs de calendários que o robô deve consultar. O ID principal é geralmente o seu endereço de e-mail.
-   `DURACAO_CONSULTA`: A duração em minutos que o evento/reunião deve ter.

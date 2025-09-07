# Robô Agendador para Google Calendar

Este projeto contém uma série de scripts Python para automatizar a gestão de agendas no Google Calendar. Ele foi projetado para encontrar horários disponíveis em uma ou mais agendas e, opcionalmente, marcar novos eventos (consultas, reuniões, etc.), atuando como um assistente de agendamento pessoal.

## Funcionalidades e Scripts do projeto

O projeto é composto pelos seguintes scripts:

-   `agendador.py`: O script principal. Ele busca por horários vagos (de acordo com uma duração definida) em uma ou mais agendas e, ao encontrar o primeiro disponível, marca uma consulta de exemplo. É o script mais completo, combinando a busca e a criação de eventos.

-   `encontra-agenda.py`: Uma versão simplificada que apenas realiza a busca por horários disponíveis e os exibe no terminal. Não realiza nenhum agendamento, sendo útil para apenas consultar a disponibilidade.

-   `teste_conexao.py`: Um script de diagnóstico para verificar se a autenticação com a API do Google Calendar está funcionando corretamente. Ele lista todas as agendas às quais a sua conta de serviço tem acesso. É o primeiro script que você deve rodar para garantir que a configuração inicial está correta.

-   `teste_escrita.py`: Um script de diagnóstico para verificar a permissão de escrita. Ele tenta criar um evento fixo na sua agenda principal. Use-o para garantir que o robô não só consegue ler, mas também criar eventos.

## Configuração e Instalação do projeto

Para utilizar este projeto, você precisará de uma conta Google e um projeto no Google Cloud Platform. Siga os passos abaixo.

### Pré-requisitos
- Python 3.6 ou superior.
- Uma conta do Google com o Google Calendar ativado.

### 1. Configuração do Projeto no Google Cloud

1.  **Crie um novo projeto** no [Google Cloud Console](https://console.cloud.google.com/).
2.  **Ative a API do Google Calendar**:
    - No menu de navegação, vá para "APIs & Services" > "Library".
    - Procure por "Google Calendar API" e clique em "Enable".
3.  **Crie uma Conta de Serviço (Service Account)**:
    - No menu de navegação, vá para "IAM & Admin" > "Service Accounts".
    - Clique em "+ CREATE SERVICE ACCOUNT".
    - Dê um nome para a conta (ex: `robo-agendador`) e clique em "CREATE AND CONTINUE".
    - **Não é necessário conceder acesso a um papel (role) neste passo**, pode clicar em "CONTINUE" e depois "DONE".
4.  **Crie uma chave JSON para a Conta de Serviço**:
    - Na lista de contas de serviço, encontre a que você acabou de criar.
    - Clique nos três pontos (Ações) e selecione "Manage keys".
    - Clique em "ADD KEY" > "Create new key".
    - Escolha o formato **JSON** e clique em "CREATE". O download de um arquivo `.json` começará automaticamente.
5.  **Renomeie e mova a chave**:
    - Renomeie o arquivo baixado para `credentials.json`.
    - Mova este arquivo para a pasta raiz deste projeto. **Este arquivo é secreto e não deve ser compartilhado ou exposto publicamente.**

### 2. Compartilhe sua Agenda

Para que o robô possa ler e escrever na sua agenda, você precisa compartilhá-la com a conta de serviço.

1.  **Encontre o e-mail da sua conta de serviço**. Ele estará nos detalhes da conta de serviço que você criou (parecido com `robo-agendador@seu-projeto.iam.gserviceaccount.com`).
2.  **Abra o Google Calendar** no seu navegador.
3.  Encontre a agenda que deseja automatizar, clique nos três pontos e vá em "Configurações e compartilhamento".
4.  Na seção "Compartilhar com pessoas específicas", clique em "Adicionar pessoas".
5.  Cole o e-mail da sua conta de serviço no campo de e-mail.
6.  Em "Permissões", selecione **"Ver todos os detalhes do evento"** (para leitura) ou **"Fazer alterações nos eventos"** (para leitura e escrita). Para o `agendador.py` e `teste_escrita.py` funcionarem, a permissão de escrita é necessária.
7.  Clique em "Enviar".

### 3. Instalação das Dependências

Este projeto utiliza bibliotecas do Google para interagir com a API. Instale-as usando `pip`:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Como Usar

Depois de concluir a configuração, você pode executar os scripts.

### 1. Verifique a Conexão

Primeiro, rode o script `teste_conexao.py` para garantir que o robô consegue se autenticar e acessar as agendas que você compartilhou.

```bash
python teste_conexao.py
```
O resultado deve ser uma lista com os nomes das suas agendas.

### 2. Verifique a Permissão de Escrita

Em seguida, rode `teste_escrita.py` para confirmar que o robô pode criar eventos.

```bash
python teste_escrita.py
```
Se tudo der certo, um novo evento de teste chamado "Reunião de Alinhamento" aparecerá na sua agenda principal 5 minutos no futuro.

### 3. Encontre Horários ou Agende Consultas

-   Para **apenas ver** os horários disponíveis:
    ```bash
    python encontra-agenda.py
    ```
-   Para **encontrar e agendar** uma consulta no primeiro horário livre:
    ```bash
    python agendador.py
    ```

### Configurando os Scripts

Dentro dos arquivos `agendador.py` e `encontra-agenda.py`, você pode customizar as seguintes variáveis no início do script:

-   `meus_calendarios`: Uma lista de IDs de calendários que o robô deve consultar. O ID principal é geralmente o seu endereço de e-mail.
-   `duracao_consulta`: A duração em minutos que o evento/reunião deve ter.
-   `inicio_busca` e `fim_busca`: O período em que o robô deve procurar por horários. Por padrão, ele busca nos próximos 7 dias.

No script `agendador.py`, você também pode alterar os detalhes do paciente/evento a ser marcado na seção `if __name__ == '__main__':`.

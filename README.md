
# Pulse Fit

**Pulse Fit** é um sistema desenvolvido em Flask para gerenciar academias, incluindo funcionalidades como check-ins de alunos, geração de relatórios, envio de e-mails e monitoramento de alunos em risco.

---

## 📋 Funcionalidades

- **Check-in de Alunos**: Registro de entrada e saída dos alunos.
- **Relatórios**: Geração de relatórios em formato `.txt` e envio por e-mail.
- **Fila de Processamento**: Uso do RabbitMQ para processamento assíncrono de tarefas.
- **Monitoramento de Alunos em Risco**: Identificação de alunos com baixa frequência.
- **Integração com Banco de Dados**: Suporte a PostgreSQL.
- **Envio de E-mails**: Configuração para envio de relatórios via Gmail ou outros provedores SMTP.

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask
- **Banco de Dados**: PostgreSQL
- **Mensageria**: RabbitMQ
- **Frontend**: HTML, CSS (Bootstrap)
- **Outros**:
  - Flask-Mail
  - Flask-Migrate
  - SQLAlchemy
  - APScheduler

---

## 🚀 Como Executar o Projeto

### ⚙️ Pré-requisitos

- Python 3.9 ou superior
- PostgreSQL
- RabbitMQ
- Ambiente virtual configurado (`venv`)

### 📦 Passos para rodar localmente

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/pulse-fit.git
   cd pulse-fit
   ```

2. **Crie e ative o ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/MacOS
   venv\Scripts\activate           # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o banco de dados no PostgreSQL**:

   No seu PostgreSQL, crie o banco chamado `pulsefit`:
   ```sql
   CREATE DATABASE pulsefit;
   ```

5. **Configure as credenciais do banco em `academia/__init__.py`**:
   ```python
   app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://usuario:senha@localhost:5432/pulsefit"
   ```

6. **Gere as migrações e aplique-as**:
   ```bash
   flask db init        # (se ainda não foi iniciado)
   flask db migrate -m "Criação das tabelas"
   flask db upgrade
   ```

7. **Popule o banco de dados com dados iniciais**:
   ```bash
   python gerar_dados_para_db.py
   ```

8. **Inicie o RabbitMQ**:
   Certifique-se de que o RabbitMQ está em execução:
   ```bash
   rabbitmq-server
   ```

9. **Execute a aplicação**:
   ```bash
   python run.py
   ```

10. **Acesse no navegador**:
    ```
    http://127.0.0.1:5000
    ```

---

## 📧 Configuração de E-mail

Para envio de relatórios por e-mail, configure as credenciais SMTP no `academia/__init__.py`:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'sua_senha_de_aplicativo'
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'
```

---

## 📂 Estrutura do Projeto

```
Pulse_Fit/
├── academia/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   │   ├── aluno_risco.html
│   │   └── ...
│   ├── relatorio/
│   │   ├── utils.py
│   │   ├── worker_relatorio.py
│   │   ├── agendador.py
│   │   └── relatorio_alunos.py
├── gerar_dados_para_db.py
├── run.py
├── requirements.txt
└── README.md
```

---

## 📜 Licença

Este projeto está sob a licença MIT. Sinta-se à vontade para usá-lo e modificá-lo.

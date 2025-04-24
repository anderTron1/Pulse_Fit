from faker import Faker
from datetime import datetime, timedelta, timezone
import random
from tqdm import tqdm
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///instance/pulsefit.db')

#engine = create_engine('postgresql://postgres:123@localhost:5432/pulsefit')

fake = Faker('pt_BR')

def gerar_planos():
    # Lista dos dados fornecidos
    planos_dados = [
        ("Plano Fit", 99.99, "Acesso total à academia (segunda a sábado);Aulas coletivas;Avaliação física", "Mensal"),
        ("Plano Black", 149.9, "Acesso total à academia (segunda a sábado);Aulas coletivas;Personal trainer;Avaliação física;Camiseta Pulse Fit", "Mensal"),
        ("Plano Básico", 79.9, "Acesso total à academia (segunda a sábado)", "Mensal"),
        ("Plano Básico", 239.7, "Acesso total à academia (segunda a sábado)", "Trimestral"),
        ("Plano Fit", 299.7, "Acesso total à academia (segunda a sábado);Aulas coletivas;Avaliação física", "Trimestral"),
        ("Plano Black", 404.73, "Acesso total à academia (segunda a sábado);Aulas coletivas;Personal trainer;Avaliação física;Camiseta Pulse Fit", "Trimestral"),
        ("Plano Básico", 407.49, "Acesso total à academia (segunda a sábado)", "Semestral"),
        ("Plano Fit", 509.49, "Acesso total à academia (segunda a sábado);Aulas coletivas;Avaliação física", "Semestral"),
        ("Plano Black", 764.49, "Acesso total à academia (segunda a sábado);Aulas coletivas;Personal trainer;Avaliação física;Camiseta Pulse Fit", "Semestral"),
        ("Plano Básico", 767.04, "Acesso total à academia (segunda a sábado)", "Anual"),
        ("Plano Fit", 959.04, "Acesso total à academia (segunda a sábado);Aulas coletivas;Avaliação física", "Anual"),
        ("Plano Black", 1439.04, "Acesso total à academia (segunda a sábado);Aulas coletivas;Personal trainer;Avaliação física;Camiseta Pulse Fit", "Anual"),
    ]

    comandos_sql = []

    for plano, preco, descricao, categoria in planos_dados:
        ativo = random.choice([True, False])
        # Alteração aqui para usar timezone-aware datetime
        dtcadastro = fake.date_time_between(start_date='-1y', end_date=datetime.now(timezone.utc)).strftime('%Y-%m-%d %H:%M:%S')
        descricao_sql = descricao.replace("'", "''")  # Escapar apóstrofos
        comando = f"""
    INSERT INTO plano (ativo, dtcadastro, plano, preco, categoria, descricao)
    VALUES ({True}, '{dtcadastro}', '{plano}', {preco}, '{categoria}', '{descricao_sql}');
    """.strip()
        comandos_sql.append(comando)
    return comandos_sql, len(planos_dados)

def gerar_clientes(quantidade_clientes, utlimo_id_plano):
    # Conjuntos para garantir unicidade
    unique_cpfs = set()
    unique_rgs = set()
    unique_emails = set()

    clientes_sql = []

    while len(clientes_sql) < quantidade_clientes:
        nome = fake.first_name()
        sobrenome = fake.last_name()
        genero = random.choice(['M', 'F'])

        # Gerar CPF único
        cpf = fake.random_int(min=10000000000, max=99999999999)
        while cpf in unique_cpfs:  # Garantir unicidade
            cpf = fake.random_int(min=10000000000, max=99999999999)
        unique_cpfs.add(cpf)

        # Gerar RG único
        rg = fake.random_int(min=1000000, max=9999999)
        while rg in unique_rgs:  # Garantir unicidade
            rg = fake.random_int(min=1000000, max=9999999)
        unique_rgs.add(rg)

        # Gerar email único
        email = fake.email()
        while email in unique_emails:  
            email = fake.email()
        unique_emails.add(email)

        dt_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        estado_civil = random.choice(['Solteiro', 'Casado', 'Divorciado', 'Viúvo'])
        telefone = fake.random_int(min=10000000000, max=99999999999)
        rua = fake.street_name()
        numero = fake.building_number()
        complemento = 'Apto 101'
        bairro = fake.bairro()
        cidade = fake.city()
        estado = fake.estado_nome()
        plano_id = random.randint(1, utlimo_id_plano)

        # Alteração aqui para usar timezone-aware datetime
        dtcadastro = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        sql = f"""INSERT INTO cliente (ativo, dtcadastro, nome, sobrenome, genero, cpf, rg, dt_nascimento, estado_civil, 
    email, telefone, rua, numero, complemento, bairro, cidade, estado, plano) VALUES 
    (TRUE, '{dtcadastro}', '{nome.replace("'", "")}', '{sobrenome.replace("'", "")}', '{genero}', {cpf}, {rg}, 
    '{dt_nascimento}', '{estado_civil}', '{email}', {telefone}, '{rua.replace("'", "")}', {numero}, '{complemento.replace("'", "")}', 
    '{bairro.replace("'", "")}', '{cidade.replace("'", "")}', '{estado.replace("'", "")}', {plano_id});"""

        clientes_sql.append(sql)

    return clientes_sql

def gerar_checkin(qtd_ids_clientes, quantidade_checkins):
    checkins_sql = []

    # Supondo que os clientes existentes estão com ids de 1 até 50
    clientes_ids = list(range(1, qtd_ids_clientes+1))  # IDs de clientes, aqui estamos gerando 50 checkins

    # Função para gerar uma lista aleatória de dias de falta
    def gerar_dias_falta():
        # Vamos gerar de 0 a 3 faltas na semana
        num_faltas = random.randint(0, 3)
        dias_da_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dias_faltas = random.sample(dias_da_semana, num_faltas)  # Selecionar dias aleatórios de falta
        return dias_faltas

    def gerar_hora_aleatoria():
        """Função para gerar um horário aleatório (hora e minuto)"""
        hora = random.randint(6, 19)  # Gerando hora entre 6h e 23h
        minuto = random.randint(0, 59)  # Gerando minuto entre 0 e 59
        return f"{hora:02}:{minuto:02}"  # Retorna no formato HH:mm"


    while len(checkins_sql) < quantidade_checkins:
        cliente_id = random.choice(clientes_ids)
    
        # Gerar data de check-in (vamos começar o check-in em um dia aleatório de uma semana)
        dt_checkin = fake.date_this_year(before_today=True, after_today=False)
        
        # Gerar dias de falta para o cliente (0 a 3 dias de falta na semana)
        dias_falta = gerar_dias_falta()
        
        # Gerar dados de check-in e check-out para a semana inteira (7 dias)
        for i in range(7):  # Vamos gerar check-ins para uma semana inteira (7 dias)
            if dt_checkin + timedelta(days=i) < datetime.now().date():
                dia_semana = (dt_checkin + timedelta(days=i)).strftime('%A')  # Obter o dia da semana
                
                # Se o dia for um dia de falta, o cliente não irá comparecer
                if dia_semana in dias_falta:
                    continue  # Não cria check-in para esse dia

                # Gerar hora e minuto para check-in
                hora_checkin_str = gerar_hora_aleatoria()  # Gerar hora para check-in
                hora_checkout_str = gerar_hora_aleatoria()  # Gerar hora para check-out
                
                # Convertendo para datetime para manipulação de horas
                hora_checkin_obj = datetime.strptime(hora_checkin_str, "%H:%M")

                hora_checkout_obj = hora_checkin_obj + timedelta(hours=random.randint(1, 4))

                # Gerar o horário completo de check-in e check-out
                dt_checkin_completo_str = f"{dt_checkin + timedelta(days=i)} {hora_checkin_str}"
                dt_checkout_completo_str = f"{dt_checkin + timedelta(days=i)} {hora_checkout_obj.strftime('%H:%M')}"
                
                # Converter para datetime para utilizar no banco
                dt_checkin_completo = datetime.strptime(dt_checkin_completo_str, "%Y-%m-%d %H:%M")
                dt_checkout_completo = datetime.strptime(dt_checkout_completo_str, "%Y-%m-%d %H:%M")

                # Inserir os dados na tabela Checkin
                sql = f"""INSERT INTO checkin (dt_checkin, dt_checkout, cliente_id) VALUES 
        ('{dt_checkin_completo}', '{dt_checkout_completo}', {cliente_id});"""
                
                checkins_sql.append(sql)
    return checkins_sql

if __name__ == "__main__":
    # Gerar comandos SQL para planos
    qtd_cliente = 50
    qtd_checkin = 4000
    planos_sql, qtd_planos = gerar_planos()
    clientes_sql = gerar_clientes(qtd_cliente, qtd_planos)
    checkins_sql = gerar_checkin(qtd_cliente, qtd_checkin)

    with engine.begin() as connection:
        print("[X] GERANDO PLANOS...")
        for comando in tqdm(planos_sql, desc="Processando planos", unit="plano"):
            connection.execute(text(comando))

    with engine.begin() as connection:
        print("[X] GERANDO CLIENTES...")
        for comando in tqdm(clientes_sql, desc="Processando clientes", unit="cliente"):
           connection.execute(text(comando))

    with engine.begin() as connection:
        print("[X] GERANDO CHECKINS...")
        for comando in tqdm(checkins_sql, desc="Processando check-ins", unit="check-in"):
            connection.execute(text(comando))
        
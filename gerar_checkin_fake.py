from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker('pt_BR')

checkins_sql = []

# Supondo que os clientes existentes estão com ids de 1 até 50
clientes_ids = list(range(1, 51))  # IDs de clientes, aqui estamos gerando 50 checkins

# Função para gerar uma lista aleatória de dias de falta
def gerar_dias_falta():
    # Vamos gerar de 0 a 3 faltas na semana
    num_faltas = random.randint(0, 3)
    dias_da_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dias_faltas = random.sample(dias_da_semana, num_faltas)  # Selecionar dias aleatórios de falta
    return dias_faltas

def gerar_hora_aleatoria():
    """Função para gerar um horário aleatório (hora e minuto)"""
    hora = random.randint(6, 23)  # Gerando hora entre 6h e 23h
    minuto = random.randint(0, 59)  # Gerando minuto entre 0 e 59
    return f"{hora:02}:{minuto:02}"  # Retorna no formato HH:mm"

while len(checkins_sql) < 2000:
    cliente_id = random.choice(clientes_ids)
    
    # Gerar data de check-in (vamos começar o check-in em um dia aleatório de uma semana)
    dt_checkin = fake.date_this_year(before_today=True, after_today=False)
    
    # Gerar dias de falta para o cliente (0 a 3 dias de falta na semana)
    dias_falta = gerar_dias_falta()
    
    # Gerar dados de check-in e check-out para a semana inteira (7 dias)
    for i in range(7):  # Vamos gerar check-ins para uma semana inteira (7 dias)
        dia_semana = (dt_checkin + timedelta(days=i)).strftime('%A')  # Obter o dia da semana
        
        # Se o dia for um dia de falta, o cliente não irá comparecer
        if dia_semana in dias_falta:
            continue  # Não cria check-in para esse dia

        # Gerar hora e minuto para check-in e check-out
        hora_checkin = gerar_hora_aleatoria()  # Gerar hora para check-in
        checkout_days = random.randint(1, 2)  # O check-out será entre 1 e 2 dias após o check-in
        hora_checkout = gerar_hora_aleatoria()  # Gerar hora para check-out
        
        # Gerar o horário completo de check-in e check-out
        dt_checkin_completo = f"{dt_checkin + timedelta(days=i)} {hora_checkin}"
        dt_checkout_completo = f"{dt_checkin + timedelta(days=i + checkout_days)} {hora_checkout}"
        
        # Inserir os dados na tabela Checkin
        sql = f"""INSERT INTO checkin (dt_checkin, dt_checkout, cliente_id) VALUES 
('{dt_checkin_completo}', '{dt_checkout_completo}', {cliente_id});"""
        
        checkins_sql.append(sql)

# Salvar em arquivo .sql
with open("inserts_checkins.sql", "w", encoding="utf-8") as f:
    f.write("\n\n".join(checkins_sql))

print("Arquivo 'inserts_checkins.sql' gerado com sucesso!")

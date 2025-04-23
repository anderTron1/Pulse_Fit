from faker import Faker
from datetime import datetime
import random

fake = Faker('pt_BR')

# Conjuntos para garantir unicidade
unique_cpfs = set()
unique_rgs = set()
unique_emails = set()

clientes_sql = []

while len(clientes_sql) < 50:
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
    plano_id = random.randint(1, 5)

    dtcadastro = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    sql = f"""INSERT INTO cliente (ativo, dtcadastro, nome, sobrenome, genero, cpf, rg, dt_nascimento, estado_civil, 
email, telefone, rua, numero, complemento, bairro, cidade, estado, plano) VALUES 
(TRUE, '{dtcadastro}', '{nome}', '{sobrenome}', '{genero}', {cpf}, {rg}, 
'{dt_nascimento}', '{estado_civil}', '{email}', {telefone}, '{rua}', {numero}, '{complemento}', 
'{bairro}', '{cidade}', '{estado}', {plano_id});"""

    clientes_sql.append(sql)

# Salvar em arquivo .sql
with open("inserts_clientes.sql", "w", encoding="utf-8") as f:
    f.write("\n\n".join(clientes_sql))

print("Arquivo 'inserts_clientes.sql' gerado com sucesso!")

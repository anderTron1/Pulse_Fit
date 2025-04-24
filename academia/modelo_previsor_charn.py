import pandas as pd 
from academia import app, db 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve
from sklearn.preprocessing import LabelEncoder
from academia.models import Cliente, Checkin, Plano
import numpy as np
import warnings
from sqlalchemy import func, distinct

import joblib

# Subconsulta com os campos agregados por cliente e semana

def executar_subconsulta(id_cliente=None):
    if id_cliente:
        print(f"[X] - Extraindo dados do cliente {id_cliente}...")
    else:
        print("[X] - Extraindo dados para treinamento...")
    query = (
        db.session.query(
            Cliente.id.label("id"),
            Cliente.nome.label("nome"),
            func.strftime('%m-%W', Checkin.dt_checkin).label("mes_semana"),
            func.count(distinct(func.date(Checkin.dt_checkin))).label("dias_presentes"),
            func.max(Checkin.dt_checkin).label("ultimo_checkin"),
            func.round(
                func.julianday(func.current_date()) - func.julianday(func.max(Checkin.dt_checkin))
            ).label("dias_desde_ultimo_checkin"),
            func.round(
                func.avg((func.julianday(Checkin.dt_checkout) - func.julianday(Checkin.dt_checkin)) * 24), 2
            ).label("duracao_media_horas"),
            Plano.id.label("id_plano"),
            Plano.plano.label("nome_plano")
        )
        .join(Plano, Cliente.plano == Plano.id)
        .join(Checkin, Checkin.cliente_id == Cliente.id)
    )

    # Aplica o filtro se o id_cliente for informado
    if id_cliente is not None:
        query = query.filter(Cliente.id == id_cliente)

    query = query.group_by(Cliente.id, Cliente.nome, func.strftime('%m-%W', Checkin.dt_checkin))
    
    subquery = query.subquery()

    resultado = db.session.query(
        subquery.c.mes_semana,
        subquery.c.dias_presentes,
        subquery.c.dias_desde_ultimo_checkin,
        subquery.c.duracao_media_horas,
        subquery.c.nome_plano
    ).all()

    df = pd.DataFrame(resultado, columns=[
        "mes_semana",
        "dias_presentes", 
        "dias_desde_ultimo_checkin", 
        "duracao_media_horas", 
        "nome_plano"
    ])
    df['cancelou'] = df.apply(
        lambda row: 1 if row['dias_desde_ultimo_checkin'] > 30 and row['dias_presentes'] < 4 else 0, 
        axis=1
    )
    return df 

def transformar_dados(df):      
    # Transformar os dados categóricos em numéricos
    print("[X] - Transformando dados categoricos...")
    label_encoder = LabelEncoder()
    df['nome_plano'] = label_encoder.fit_transform(df['nome_plano'])
    return df, label_encoder
    
def divisao_dos_dados(df):
    print("[X] - Dividindo dados treinamento e teste...")
    x = df[['dias_presentes', 'dias_desde_ultimo_checkin', 'duracao_media_horas', 'nome_plano']]
    y = df['cancelou']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test

def treinar_modelo(x_train, y_train):
    modelo = LogisticRegression()
    modelo.fit(x_train, y_train)
    print("[X] - Treinamento finalizado...")
    return modelo

def avaliando_modelo(modelo, x_test, y_test):
    acuracia = modelo.score(x_test, y_test)
    print("[X] - Avaliando modelo...")
    print(f"Acurácia do modelo: {acuracia:.2f}")
    return acuracia

def previsao(modelo, x_test):
    previsoes = modelo.predict(x_test)
    return previsoes

def previsao_proximos_dias(modelo, cliente):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        previsoes = modelo.predict_proba(cliente)#[0][1]
        return int(np.argmax(previsoes))

def executar_novo_treino():
    print("[LOGISTIC_REGRESSION] - Executando...")
    df = executar_subconsulta()
    df = df.drop(columns=['mes_semana'])
    df, label_encoder = transformar_dados(df)
    x_train, x_test, y_train, y_test = divisao_dos_dados(df)

    modelo = treinar_modelo(x_train, y_train)
    acuracia = avaliando_modelo(modelo, x_test, y_test)
    print("[X] - Gerando e salvando modelo...")
    joblib.dump(modelo, 'modelo_treinado.pkl')

def carregar_modelo():
    # verificar se o modelo existe 
    try:
        modelo_carregado = joblib.load('modelo_treinado.pkl')
        print("[X] - Modelo carregado com sucesso.")
    except FileNotFoundError:
        print("[X] - Modelo não encontrado. Treinando novo modelo...")
        executar_novo_treino()
        # Carregar o modelo novamente após o treinamento
        modelo_carregado = joblib.load('modelo_treinado.pkl')
    return modelo_carregado
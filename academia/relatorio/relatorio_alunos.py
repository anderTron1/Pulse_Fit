import pika
import json
from academia.models import db, Checkin, Cliente  # Adapte conforme sua estrutura

def envia_relatorio_para_fila(data):
    # Busca todos os check-ins com aluno relacionado
    checkins = Checkin.query.join(Cliente).order_by(Checkin.dt_checkin.asc()).all()
    
    # Estrutura correta para os dados
    dados_checkins = [
        {
            "aluno": "andre", #c.cliente.nome,  # Nome do aluno
            "dt_checkin": c.dt_checkin.strftime("%H:%M"),
            "dt_checkout": c.dt_checkout.strftime("%H:%M")
        }
        for c in checkins
    ]

    conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    canal = conexao.channel()

    # Certifique-se de que a fila é a mesma que o worker está consumindo
    canal.queue_declare(queue="relatorio_diario", durable=True)

    mensagem = json.dumps({"checkins": dados_checkins})  # Serializa os dados como JSON

    # Publica a mensagem na fila
    canal.basic_publish(
        exchange="",
        routing_key="relatorio_diario",  # Deve ser a mesma fila que o worker consome
        body=mensagem,
        properties=pika.BasicProperties(delivery_mode=2)  # Mensagem persistente
    )

    conexao.close()
    print(f"[AGENDADOR] Relatório enviado para a fila com {len(dados_checkins)} check-ins")
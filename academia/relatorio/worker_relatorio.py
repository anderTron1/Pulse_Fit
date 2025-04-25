import pika
import json
from academia.relatorio.utils import gerar_pdf_relatorio, enviar_relatorio_por_email
from academia import app, url_CloudAMQP
from datetime import datetime

def callback(ch, method, properties, body):
    dados = json.loads(body)
    checkins = dados['checkins']
    hoje = datetime.today().date() 
    gerar_pdf_relatorio(checkins, hoje)
    enviar_relatorio_por_email('andreluizpires1507@gmail.com', checkins, hoje)

def iniciar_worker_relatorio():
    connection = pika.BlockingConnection(pika.URLParameters(url_CloudAMQP))
    channel = connection.channel()
    channel.queue_declare(queue='relatorio_diario', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='relatorio_diario', on_message_callback=callback)
    print(" [*] Aguardando mensagens...")
    channel.start_consuming()

 
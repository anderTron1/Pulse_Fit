from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from academia import app
from academia.relatorio.relatorio_alunos import envia_relatorio_para_fila
from academia.relatorio.utils import gerar_pdf_relatorio, enviar_relatorio_por_email

from multiprocessing import Process, Queue
from datetime import datetime
import json 
import pika

from academia import HORA_ENVIO_RELATORIO, MINUTOS_ENVIO_RELATORIO, EMAIL_PARA_TESTE

def iniciar_worker_relatorio(queue):
    def callback(ch, method, properties, body):
        with app.app_context():  # Garante que o contexto Flask esteja ativo
            print("[WORKER RELATÓRIO] Mensagem recebida:", body)
            try:
                dados = json.loads(body)
                checkins = dados['checkins']
                hoje = datetime.today().date()
                gerar_pdf_relatorio(checkins, hoje)
                enviar_relatorio_por_email(EMAIL_PARA_TESTE, checkins, hoje)
                print("[WORKER RELATÓRIO] Relatório gerado e enviado com sucesso.")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"[WORKER RELATÓRIO] Erro ao processar a mensagem: {e}")
            queue.put("iniciar_worker_relatorio")
    conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    canal = conexao.channel()
    canal.queue_declare(queue="relatorio_diario", durable=True)
    canal.basic_qos(prefetch_count=1)
    canal.basic_consume(queue="relatorio_diario", on_message_callback=callback)

    print("[WORKER RELATÓRIO] Aguardando mensagens...")
    canal.start_consuming()

def iniciar_agendador_com_sinal(queue):
    """Inicia o agendador e envia um sinal para a fila quando a tarefa for executada."""
    from apscheduler.schedulers.blocking import BlockingScheduler
    from datetime import datetime

    def agendar_relatorio():
        hoje = datetime.today().date()
        with app.app_context():  
            envia_relatorio_para_fila(data=hoje) 
            print(f"[AGENDADOR] Enviando tarefa para relatório de {hoje}")
            queue.put("iniciar_worker_relatorio")

    scheduler = BlockingScheduler()
    scheduler.add_job(agendar_relatorio, 'cron', hour=HORA_ENVIO_RELATORIO, minute=MINUTOS_ENVIO_RELATORIO)  
    print("[AGENDADOR] Iniciado. Relatórios serão enviados às 16:18.")
    scheduler.start()
 
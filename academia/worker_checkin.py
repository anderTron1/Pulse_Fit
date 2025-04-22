import pika 
import json 
from datetime import datetime
from academia import app, db
from academia.models import Checkin, Cliente
import multiprocessing

dt_format = "%Y-%m-%d %H:%M:%S"
def start_worker():
    with app.app_context():
        def callback(ch, method, properties, body):
            data = json.loads(body)

            novo_checkin = Checkin(
                cliente_id = data["cliente_id"],
                dt_checkin = datetime.strptime(data["dt_checkout"], dt_format),
                dt_checkout = datetime.strptime(data["dt_checkout"], dt_format)
            )
            db.session.add(novo_checkin)
            db.session.commit()
            nome_cliente = Cliente.query.get(novo_checkin.cliente_id)
            print(f"Checkin-in salvo para o cliente {nome_cliente.nome}")

            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        conexao = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        canal = conexao.channel()
        canal.queue_declare(queue="fila_checkin", durable=True)
        canal.basic_qos(prefetch_count=1)
        canal.basic_consume(queue="fila_checkin", on_message_callback=callback)

        print("[WORKER] Aguardando mensagens de checkin-in...")
        canal.start_consuming()

def iniciar_worker():
    worker_process = multiprocessing.Process(target=start_worker)
    worker_process.daemon= True
    worker_process.start()
    print("Executando aqui...")

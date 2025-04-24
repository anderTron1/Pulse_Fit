from academia import app
from academia.worker_checkin import start_worker_checkin
from multiprocessing import freeze_support
import pika 
from academia.relatorio.agendador import iniciar_worker_relatorio, iniciar_agendador_com_sinal

from multiprocessing import Process, Queue

if __name__ == "__main__":
    freeze_support()
    print("executando...")
    
    queue = Queue()
    worker_process_checkin = Process(target=start_worker_checkin)
    worker_process_checkin.daemon= True
    worker_process_checkin.start()
   
    # Inicia o processo do agendador com a fila
    worker_process_agendador = Process(target=iniciar_agendador_com_sinal, args=(queue,))
    worker_process_agendador.daemon = True
    worker_process_agendador.start()
    print("Agendador iniciado.")

    # Inicia o processo do worker_relatorio com a fila
    worker_process_relatorio = Process(target=iniciar_worker_relatorio, args=(queue,))
    worker_process_relatorio.daemon = True
    worker_process_relatorio.start()

    #worker_process_checkin.join()
    #iniciar_worker()

    app.run(debug=True)


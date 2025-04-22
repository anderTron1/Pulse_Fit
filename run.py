from academia import app
from academia.worker_checkin import iniciar_worker
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    print("executando...")
    iniciar_worker()
    app.run(debug=True)

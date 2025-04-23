from flask_mail import Mail, Message
from flask import  current_app 
#import pdfkit
import os
from academia import mail
import os

def gerar_pdf_relatorio(checkins, data, nome_arquivo="relatorio.txt"):
    # Monta o conteúdo do relatório em texto puro
    linhas = []
    linhas.append("Relatório de Frequência")
    linhas.append(f"Data do relatório: {data.strftime('%d/%m/%Y')}")
    linhas.append("")

    if checkins:
        linhas.append("Aluno\tData\tHorário de Check-in\tHorário de Check-out")
        for c in checkins:
            # Acessa os valores dos dicionários usando as chaves
            linhas.append(f"{c['aluno']}\t{c['dt_checkin']}\t{c['dt_checkin']}\t{c['dt_checkout']}")
    else:
        linhas.append("Nenhum check-in registrado.")

    conteudo = "\n".join(linhas)

    # Caminho do arquivo de saída
    caminho_arquivo = os.path.join(os.getcwd(), "academia", "relatorio", "saida", nome_arquivo)
    # Garante que o diretório existe
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    # Escreve no arquivo de texto
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo)

    return caminho_arquivo

def enviar_relatorio_por_email(destinatario, checkins, data):
    try:
        print("entrando aqui...")
        # Gerar PDF
        caminho_txt = gerar_pdf_relatorio(checkins, data)

        # Criar e-mail
        msg = Message("Relatório de Frequência", sender=destinatario,  recipients=[destinatario])
        msg.body = f"Segue em anexo o relatório de frequência de {data.strftime('%d/%m/%Y')}."
        
        # Anexar o PDF gerado
        with current_app.open_resource(caminho_txt) as f:
            msg.attach("relatorio.txt", "text/plain", f.read())

        # Enviar e-mail
        mail.send(msg)
        print(f"[AGENDADOR] Relatório enviado para {destinatario} com sucesso!")
    except Exception as e:
        print(f"[AGENDADOR] Erro ao enviar e-mail: {e}")
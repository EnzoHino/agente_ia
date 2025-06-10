from flask import Blueprint, render_template, request
from datetime import datetime
import os
from agentAI import registra_ia

bp = Blueprint("chat", __name__)

LOG_PATH = "logs.log"

def registrar_log(usuario, mensagem):
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{usuario.upper()}] {mensagem}\n")

def carregar_historico():
    historico = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for linha in f:
                texto = linha.strip()
                if "[USUARIO]" in texto:
                    tipo = "usuario"
                elif "[AGENTE]" in texto:
                    tipo = "agente"
                elif "[JUÍZ]" in texto or "[JUIZ]" in texto:
                    tipo = "juiz"
                else:
                    tipo = "sistema"
                historico.append({"texto": texto, "tipo": tipo})
    return historico

@bp.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        if "enviar" in request.form:
            msg = request.form.get("mensagem", "")
            registrar_log("usuario", msg)
            
            registra_ia(msg)
        elif "encerrar" in request.form:
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                pass
            registrar_log("sistema", "CONVERSA INICIADA")

    historico = carregar_historico()
    return render_template("index.html", historico=historico)
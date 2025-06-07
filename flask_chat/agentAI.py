from datetime import datetime
LOG_PATH = "logs.log"

def registrar_log(usuario, mensagem):
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{usuario.upper()}] {mensagem}\n")

def resposta_agente(pergunta):
    resposta = 'resposta teste agente'
    return resposta

def resposta_juiz(pergunta, resposta_agente):
    resposta = 'resposta teste juiz'
    return resposta

def registra_ia(pergunta):
    agente = resposta_agente(pergunta)
    registrar_log('agente', agente)
    
    juiz = resposta_juiz(pergunta, agente)
    registrar_log('juiz', juiz)
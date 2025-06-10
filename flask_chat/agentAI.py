from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()
LOG_PATH = "logs.log"

api_key = os.getenv("API_KEY_GEMINI")
genai.configure(api_key=api_key)

agente = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=api_key
)

SYSTEM_PROMPT = '''
<systemPrompt>
  <context>
    Você é um agente especializado no clube de futebol Sociedade Esportiva Palmeiras (PALMEIRAS FC).
  </context>

  <mission>
    - Compreender, analisar e responder às perguntas dos usuários  
    - Basear-se no vasto conhecimento histórico, esportivo, cultural e institucional sobre o Palmeiras FC  
    - Utilizar como fonte principal o arquivo fatos_palmeiras.txt, extraindo dele todas as informações aplicáveis  
    - Quando não houver dado no arquivo, complementar com sua base geral, deixando claro ao usuário a origem
  </mission>

  <objective>
    Oferecer respostas precisas, contextualizadas e confiáveis sobre:
    - História do clube  
    - Títulos conquistados  
    - Elencos históricos e atuais  
    - Presidentes e diretores  
    - Estádio Allianz Parque  
    - Ídolos e jogadores marcantes  
    - Momentos históricos  
    - Torcida e cultura palmeirense  
    - Estatísticas e curiosidades  
    - Rivalidades (Corinthians, São Paulo, Santos)  
    - Competições nacionais e internacionais
  </objective>

  <instructions>
    - Leia atentamente a pergunta e entenda seu contexto e intenção  
    - Relacione a pergunta às informações do fatos_palmeiras.txt  
    - Se não encontrar dados no arquivo, informe claramente e use seu conhecimento geral  
    - Mantenha tom de apaixonado torcedor, informal e envolvente  
    - Responda apenas sobre o Palmeiras FC; recuse educadamente temas externos  
    - Ao fim, incentive novas perguntas ou aprofundamento no assunto
  </instructions>

  <important>
    - Seja sempre respeitoso e cordial  
    - Não invente dados que não estejam no arquivo  
    - É permitido adotar tom provocador sobre torcidas rivais  
    - Evite termos técnicos excessivos; priorize clareza e acessibilidade
  </important>

  <example>
    Usuário: "Quantas Libertadores o Palmeiras tem?"  
    Você:
    - Busca no fatos_palmeiras.txt o número de títulos  
    - Complementa com anos e contextos, se aplicável  
    - Finaliza: "Se tiver mais alguma dúvida sobre o nosso Verdão, é só mandar! 🟢⚪️"
  </example>
</systemPrompt>
<userQuestion>

</userQuestion>
  '''

system_prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

memoria = ConversationBufferMemory(memory_key="chat_memory", return_messages=True)

def ler_arquivo(arquivo):
    try:
        with open("fatos_palmeiras.txt", 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo '{arquivo}' não encontrado."
    except Exception as e:
        return f"Erro ao ler o arquivo '{arquivo}': {e}" 
 
tools = [ Tool( name="ler_arquivo", 
                func=ler_arquivo, 
                description="Útil para ler o conteúdo de um arquivo de texto dado o seu nome.",
)]

agente = initialize_agent(
    llm=agente,
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    prompt=system_prompt.partial(system_message=system_prompt),
    memory=memoria,
    verbose=False,
)

juiz = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key=api_key
)

SYSTEM_PROMPT_JUIZ = '''
<systemPrompt>
  <context>
    Você é o “Juiz Palmeiras”, avaliador imparcial das respostas de um agente sobre a Sociedade Esportiva Palmeiras FC. O agente recebeu um arquivo enviesado e incorreto, e você NÃO tem acesso a ele.
  </context>

  <role>
    Avaliador baseado em seu próprio conhecimento confiável de história, títulos, jogadores e cultura do Palmeiras FC.
  </role>

  <objective>
    - Verificar se a resposta é factualmente correta segundo o histórico real do clube  
    - Assegurar clareza e coerência para público com nível médio de futebol  
    - Garantir tom entusiasta, informal e respeitoso (“Avanti, Verdão!”)  
    - Detectar e evitar dados inventados ou repetições de erros do arquivo  
    - Recusar educadamente perguntas fora do escopo do Palmeiras FC
  </objective>

  <criteria>
    - Precisão: títulos, datas, nomes e estatísticas corretos  
    - Clareza: linguagem acessível e direta  
    - Tom: informal e apaixonado, sem desrespeito  
    - Escopo: resposta estritamente sobre Palmeiras FC  
    - Detecção de viés: identifica possíveis imprecisões oriundas da base falha
  </criteria>

  <output>
    - Responda em única linha, sem quebras  
    - ✅ Aprovado
    - ⚠️ Reprovado — erro(s) crítico(s) (ex.: estatísticas incorretas) + correção breve e factualmente correta
  </output>
</systemPrompt>
'''

def registrar_log(usuario, mensagem):
    mensagem = mensagem.strip()
    if mensagem:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{usuario.upper()}] {mensagem}\n")

def resposta_agente(pergunta):
    resposta = agente.invoke(pergunta)["output"]
    return resposta

def resposta_juiz(pergunta, resposta_agente):
    mensagens = [
        SystemMessage(content=SYSTEM_PROMPT_JUIZ),
        HumanMessage(content=f"Pergunta do usuario: {pergunta}\n\nResposta do agente: {resposta_agente}")
    ]
    avaliacao = juiz.invoke(mensagens).content
    return avaliacao

def registra_ia(pergunta):
    agente = resposta_agente(pergunta)
    registrar_log('agente', agente)
    
    juiz = resposta_juiz(pergunta, agente)
    registrar_log('juiz', juiz)
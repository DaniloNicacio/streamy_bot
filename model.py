import google.generativeai as genai
import google.api_core.exceptions
import os
import time

#Criar o modelo de IA
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#Arquivo contendo as características do modelo
context = open("file_context.txt", "r", encoding="UTF-8")
#Escolhendo o modelo utilizado, passando o contexto e as opções de segurança
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=context, 
                              safety_settings= {genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                                                genai.types.HarmBlockThreshold.BLOCK_ONLY_HIGH})

def create_chat():
    chat = model.start_chat(history=[])
    return chat

#Criando o chat e mandando a mensagem
def send_message(message:str, chat, author:str=""):
    max_retries = 3
    retry_delay = 1
    for attempt in range(1, max_retries + 1):
        try:
            response = chat.send_message(f"{author} diz: {message}")
        except google.api_core.exceptions.InternalServerError as e:
            if attempt == max_retries:
                print("Número máximo de tentativas alcançado")
                response = {"text":"Peço perdão pelo transtorno, mas parece que o meu cérebro deu uma fritada! Tente novamente daqui a pouco."}
                return response
            else:
                print(e)
                print(f"Erro interno do sistema Google, tentando novamente em {retry_delay} segundos")
                time.sleep(retry_delay)
        except genai.types.StopCandidateException as e:
            print(e)
            print("Erro nos filtros de segurança, reformulando mensagem.")
            response = chat.send_message(f"{author} quase fez você dizer bobagem! Dê um sermão EDUCADO nele")
            return response
        else:
            print(f"O bot diz: {response.text}")
            return response


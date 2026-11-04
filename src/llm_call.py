from math import ceil
import os, glob, time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")
MODEL = os.getenv("MODEL_LLM")
KEY = os.getenv("API_KEY")
PASTA_DESTINO = os.getenv("PATH_PASTA_DESTINO")
KEY_GPT = os.getenv("KEY_GPT")
GPT_MODEL = os.getenv("MODEL_GPT")
FLAG = int(os.getenv("FLAG_MODEL", "1"))


class CallLLM:
    
    def __init__(self, provedor: int = FLAG):
        self.provedor = provedor
        
        if self.provedor == 1:
            self.client = genai.Client(api_key=KEY)
            self.modelo_nome = MODEL
        elif self.provedor == 2:
            self.client = OpenAI(api_key=KEY_GPT)
            self.modelo_nome = GPT_MODEL
        else:
            raise ValueError("Provedor inválido. Use 1 para Gemini ou 2 para GPT.")
        
    
    def resumir_noticia(self, texto: str, tentativas: int = 3) -> str:
        prompt = f""" 
        Você é um assistente especialista em síntese de notícias e inteligência de tendências.
        Analise a matéria abaixo e produza:
        1. Um título resumido e direto.
        2. Os 3 a 5 pontos-chave da matéria (em marcadores/bullet points).
        3. O impacto ou conclusão principal em 1 frase.

        Texto da notícia:
        ---
        {texto}
        ---
        
        """
        if self.provedor == 1:
            for tentativa in range(1, tentativas + 1):
                        try:
                            response = self.client.models.generate_content(
                                    model=MODEL,
                                    contents=prompt
                                )
                            if response.text:
                                return response.text
                            raise ValueError("A resposta da LLM veio vazia...")
                        except Exception as e:
                            if tentativa < tentativas and "503" in str(e):
                                tempo_espera = tentativa *4
                                print(f"Servidor ocupado (503). Nova tentativa em {tempo_espera}.")
                                time.sleep(tempo_espera)
                            else:
                                raise e
        elif self.provedor == 2:
            response = self.client.chat.completions.create(
            model=self.modelo_nome,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente especialista em síntese de"
                        " notícias."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            )
            return response.choices[0].message.content
    
    def listar_noticias(self):
        arquivos = sorted(glob.glob(os.path.join(PASTA_DESTINO, "news_sum_url_*.txt")))
        count_news = len(arquivos)
        
        for i, path_file in enumerate(arquivos, start=1):
            file_name = os.path.basename(path_file)
            print("**********************************************************")
            print(f"[{i}/{len(arquivos)}] Processando: {path_file}")
            print("**********************************************************")
            
            try:
                with open(path_file, "r", encoding="utf-8") as f:
                    conteudo = f.read().strip()
                    
                    resumo = self.resumir_noticia(conteudo)
                    
                    # print("\n"+resumo+"\n")
                    salva_resumo = os.path.join(PASTA_DESTINO, f"resumo_{file_name}")
                    with open(salva_resumo, "w", encoding="utf-8") as out:
                        out.write(resumo)
            except Exception as e:
                print(f"Erro ao processar o arquivo {file_name}: {e}")


    def concatenar_resumos(self, txt_busca: str = "resumo_*.txt", 
                        final_file: str = "resumos_compilados.txt"):
        arquivos = sorted(glob.glob(os.path.join(PASTA_DESTINO, txt_busca)))
        num_arquivos = len(arquivos)
        
        if not arquivos:                  
            return print("Nenhum arquivo encontrado! Insira links de noticias para os resumos.")
        
        path_final = os.path.join(PASTA_DESTINO, final_file)
        
        divisor_txt = "="*100
        
        with open(path_final, "w", encoding="utf-8") as out:
            for path in arquivos:
                nome_base = os.path.basename(path)
                
                with open(path, "r", encoding="utf-8") as f:
                    conteudo = f.read().strip()
                
                out.write(f"{divisor_txt}\n")
                out.write(f"{nome_base:=^100}\n")
                out.write(f"{divisor_txt}\n")
                out.write(f"{conteudo}\n")
                out.write(f"{divisor_txt}\n\n")
        return path_final
    
    def limpar_temporarios(self):
        padroes = ["news_sum_url_*.txt", "resumo_*.txt"]
        arquivos_removidos = 0

        for padrao in padroes:
            caminho_busca = os.path.join(PASTA_DESTINO, padrao)
            for arquivo in glob.glob(caminho_busca):
                caminho_completo = os.path.abspath(arquivo)
                try:
                    os.remove(caminho_completo)
                    arquivos_removidos += 1
                except Exception as e:
                    print(f"Erro ao deletar {arquivo}: {e}")

            
    def print_monitor(self, file_name: str = "resumos_compilados.txt"):
        caminho_final = os.path.join(PASTA_DESTINO, file_name)
        
        if not os.path.exists(caminho_final):
            print(f"Arquivo '{file_name}' não encontrado em {PASTA_DESTINO}.")
            return

        with open(caminho_final, "r", encoding="utf-8") as f:
            print("\n" + f.read())
        
    
                
            
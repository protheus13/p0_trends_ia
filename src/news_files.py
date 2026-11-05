""" 
Aqui escolhe se a noticia será de apenas um link ou se ela deve ler 
um arquivo txt com vários links de noticias a serem resumidas.
"""

# importa bibliotecas

import os, time, trafilatura
from pathlib import Path
from dotenv import load_dotenv

DIRETORIO = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=DIRETORIO / ".env")

class NewsExtract:

    def le_noticias(self):
        LINKS = os.getenv("PATH_LINKS", "news_links.txt")
        PASTA_DESTINO = os.getenv("PATH_PASTA_DESTINO")
        try:
            with open(LINKS, "r", encoding="utf-8") as f:
                links = [linha.strip() for linha in f if linha.strip()]
        except FileNotFoundError:
            print(f"Erro, o arquivo com os links nao existe, crie-o.")
            exit(1)
                
        total_links = len(links)
        
        for i, url in enumerate(links, start=1):
            print(f"Percentual baixado: [{i}/{total_links}] | URL: {url}")
                
            # baixa o conteudo do link
            download = trafilatura.fetch_url(url)
            # extrai o texto
            texto = trafilatura.extract(download)
                
            # cria um arquivo para cada noticia resumida
            news_sum = os.path.join(PASTA_DESTINO, f"news_sum_url_{i:03d}.txt")
                
            with open(news_sum, "w", encoding="utf-8") as out:
                out.write(f"\nFonte da notícia: {url}\n")
                out.write(texto)
                
            # delay para evitar requisicoes em massa
            time.sleep(1)
import llm_call, news_files, time, subprocess
from pathlib import Path

c1 = llm_call.CallLLM()
e1 = news_files.NewsExtract()

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_LINKS = BASE_DIR / "data" / "news_links.txt"

# ARQUIVO_LINKS = "../data/news_links.txt"
subprocess.run(["nano", ARQUIVO_LINKS])
input(
    "\nPressione enter para iniciar o resumo das notícias dos links informados..."
)

e1.le_noticias()
time.sleep(1)
c1.listar_noticias()
c1.concatenar_resumos()
c1.limpar_temporarios()
c1.print_monitor()
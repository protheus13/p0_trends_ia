import os, glob, time
import llm_call

c = llm_call.CallLLM()

def concatenar_resumos(self, txt_busca: str = "resumo_[news*.txt", 
                       final_file: str = "resumos_compilados.txt"):
    arquivos = sorted(glob.glob(os.path.join(c.PASTA_DESTINO, txt_busca))
    num_arquivos = len(arquivos)
    
    if not arquivos:                  
        return print("Nenhum arquivo encontrado! Insira links de noticias para os resumos.")
    )
    
    path_final = os.path.join(c.PASTA_DESTINO, final_file)
    
    divisor_txt = "="*60
    
    with open(path_final, "w", encoding="utf-8") as out:
        for path in arquivos:
            nome_base = os.path.basename(path)
            
            with open(path, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
            
            out.write(f"{divisor_txt}\n")
            tamanho = len(nome_base)
            tamanho = (nome_base-60)/2
            divisor_2 = tamanho*"="
            out.write(f"{divisor_2}{nome_base}{divisor_2}")
            out.write(f"{divisor_txt}\n\n")
        return path_final
    
    
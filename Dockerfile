FROM python:3.12-slim

# Define diretório de trabalho
WORKDIR /app

# Instala o nano para suportar a edição do news_links.txt dentro do container
RUN apt-get update && apt-get install -y nano && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY . .

# Comando padrão ao rodar o container
CMD ["python", "src/main.py"]
# Atividade P0 - Primeiro Fluxo com LLM
## Problema escolhido
- Aplicação para resumir notícias diversas usando LLM com intuito de selecionar com mais efetividade qual notícia se aprofundar para se manter atualizado. Nome da aplicação "BotSum: Resumir Notícias Diversas com LLM".

## Usuário ou público
O projeto foi idealizado pensando em profissionais que gostam de se manter atualizados com as notícias de sua preferência. Contudo, algumas notícias podem ser muito prolixas ou mesmo não ter conteúdo com a profundidade necessária. Assim, a aplicação de resumo de notícias mantém o profissional atualizado ganhando tempo e, quando ulgar necessário, pode aprofundar a leitura na notícia real após a prévia enviada pela aplicação.

## Justificativa de utilização de LLM
A LLM se justifica pela capacidade de resumir conteúdos com qualidade, preservando as informações mais relevantes e gerando contexto suficiente para o entendimento da reportagem.

## Funcionamento da solução
A aplicação roda um script python que permite inserir liks de sites com reportagens de seu interesse e fazer resumos ágeis e úteis para se manter atualizado otimizando o tempo.

## Limites do projeto
O projeto em si tem várias limitações, são elas:
- Aplicação fechada;
- Sem interface WEB amigável;
- Alguns tratamentos de erros e exceções foram simplificados devido ao tempo hábil para realização.

## Passo a passo para instalação
### Instalação do docker
Caso sua máquina já possua docker, ignore este passo. Caso não tenha, execute os comandos a seguir:

- sudo apt update && sudo apt upgrade -y
- sudo apt install docker.io -y
- sudo systemctl start docker
- sudo systemctl enable docker
- sudo systemctl status docker

Após finalizar, siga para o próximo passo.
### Clonagem de repositório e configurações iniciais
- git clone https://github.com/protheus13/p0_trends_ia.git
- cp .env.example .env
Atualize as informações das chaves de API e modelos de LLM que serão utilizados.

### Etapas com docker
- docker-compose build
- docker-compose run --rm news_pipeline

### Execução do script
Ao executar os comandos do docker irá abrir um arquivo .txt com nano. A partir dái, insira os links das notícias e logo após inserir, pressione enter para saltar a linha e pode inserir quantos links quiser seguindo essa orientação. Ao final, pressione "control+x" e confirme com "y". Depois só aguardar a execução do script que irá coletar as notícias, enviar chamadas para uma LLM escolhida com o objetivo de obter um resumo das mesmas, imprimí-la na tela e salvar um arquivo final na pasta data com as últimas notícias compiladas.
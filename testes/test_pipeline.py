""" 

O arquivo de testes foi 100% gerado por IA (Gemini Pro). O procedimento e prompt utilizado
foram anexar um pdf com os requisitos do P0 para os testes, os scripts já realizados para
o projeto e solicitado que desenvolvesse um script para realização dos testes de acordo
com os requisitos informados no pdf. Ao final, conferi o código e testei a implementação
que obteve sucesso.

"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Adiciona a pasta 'src' ao sys.path para permitir a importação direta dos módulos
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from llm_call import CallLLM
from news_files import NewsExtract


class TestPipelineSemTokens(unittest.TestCase):

  def setUp(self):
    """Cria um diretório temporário para isolar os testes de arquivos."""
    self.test_dir = tempfile.TemporaryDirectory()
    self.pasta_destino = self.test_dir.name

  def tearDown(self):
    """Limpa a pasta temporária após a execução de cada teste."""
    self.test_dir.cleanup()

  # -------------------------------------------------------------------------
  # 1. Testes de Validação e Regras de Negócio Locais
  # -------------------------------------------------------------------------

  def test_provedor_invalido_gera_erro(self):
    """Garante que provedores não suportados disparem exceção controlada."""
    with self.assertRaises(ValueError):
      CallLLM(provedor=99)

  def test_concatenar_resumos_sem_arquivos(self):
    """Verifica o comportamento quando nenhum resumo existe para concatenar."""
    with patch("llm_call.PASTA_DESTINO", self.pasta_destino):
      # Instancia mockando a chamada de inicialização do cliente
      with patch("llm_call.genai.Client"):
        llm = CallLLM(provedor=1)
        resultado = llm.concatenar_resumos()
        self.assertIsNone(resultado)

  def test_concatenar_resumos_com_arquivos(self):
    """Testa a concatenação correta de resumos em um único compilado."""
    # Cria arquivos simulados de resumo
    resumo_1 = os.path.join(self.pasta_destino, "resumo_news_001.txt")
    resumo_2 = os.path.join(self.pasta_destino, "resumo_news_002.txt")

    with open(resumo_1, "w", encoding="utf-8") as f:
      f.write("Conteudo da noticia 1")
    with open(resumo_2, "w", encoding="utf-8") as f:
      f.write("Conteudo da noticia 2")

    with patch("llm_call.PASTA_DESTINO", self.pasta_destino):
      with patch("llm_call.genai.Client"):
        llm = CallLLM(provedor=1)
        caminho_final = llm.concatenar_resumos()

        self.assertTrue(os.path.exists(caminho_final))
        with open(caminho_final, "r", encoding="utf-8") as f:
          conteudo_compilado = f.read()

        self.assertIn("Conteudo da noticia 1", conteudo_compilado)
        self.assertIn("Conteudo da noticia 2", conteudo_compilado)

  def test_limpar_temporarios(self):
    """Testa se a função remove apenas arquivos temporários e preserva outros."""
    temp_news = os.path.join(self.pasta_destino, "news_sum_url_001.txt")
    temp_resumo = os.path.join(self.pasta_destino, "resumo_001.txt")
    arquivo_fixo = os.path.join(self.pasta_destino, "news_links.txt")

    for arq in [temp_news, temp_resumo, arquivo_fixo]:
      with open(arq, "w", encoding="utf-8") as f:
        f.write("conteudo")

    with patch("llm_call.PASTA_DESTINO", self.pasta_destino):
      with patch("llm_call.genai.Client"):
        llm = CallLLM(provedor=1)
        llm.limpar_temporarios()

        self.assertFalse(os.path.exists(temp_news))
        self.assertFalse(os.path.exists(temp_resumo))
        self.assertTrue(os.path.exists(arquivo_fixo))

  # -------------------------------------------------------------------------
  # 2. Testes Simulados de LLM (Mock - ZERO Consumo de Tokens)
  # -------------------------------------------------------------------------

  @patch("llm_call.genai.Client")
  def test_resumo_gemini_sucesso_mock(self, mock_client_class):
    """Simula resposta da API Gemini com sucesso."""
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "1. Titulo Mock\n2. Pontos-chave\n3. Conclusao"
    mock_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_instance

    llm = CallLLM(provedor=1)
    resumo = llm.resumir_noticia("Texto de teste da materia")

    self.assertIn("1. Titulo Mock", resumo)
    mock_instance.models.generate_content.assert_called_once()

  @patch("llm_call.OpenAI")
  def test_resumo_openai_sucesso_mock(self, mock_openai_class):
    """Simula resposta da API OpenAI com sucesso."""
    mock_instance = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "1. Titulo GPT Mock"
    mock_instance.chat.completions.create.return_value.choices = [mock_choice]
    mock_openai_class.return_value = mock_instance

    llm = CallLLM(provedor=2)
    resumo = llm.resumir_noticia("Texto de teste da materia")

    self.assertEqual(resumo, "1. Titulo GPT Mock")
    mock_instance.chat.completions.create.assert_called_once()

  @patch("llm_call.genai.Client")
  def test_resposta_vazia_llm_gera_excecao(self, mock_client_class):
    """Garante tratamento quando o modelo retorna resposta em branco."""
    mock_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = ""  # Resposta vazia
    mock_instance.models.generate_content.return_value = mock_response
    mock_client_class.return_value = mock_instance

    llm = CallLLM(provedor=1)
    with self.assertRaises(ValueError):
      llm.resumir_noticia("Texto qualquer", tentativas=1)

  # -------------------------------------------------------------------------
  # 3. Teste Simulado do Scraper (Sem chamadas reais de rede)
  # -------------------------------------------------------------------------

  @patch("news_files.trafilatura.fetch_url")
  @patch("news_files.trafilatura.extract")
  def test_extracao_noticia_sucesso_mock(self, mock_extract, mock_fetch):
    """Simula download e extração do trafilatura sem acessar a internet."""
    links_file = os.path.join(self.pasta_destino, "news_links.txt")
    with open(links_file, "w", encoding="utf-8") as f:
      f.write("https://exemplo.com/noticia-teste\n")

    mock_fetch.return_value = "<html>Noticia</html>"
    mock_extract.return_value = "Texto extraido com sucesso da materia."

    with (
        patch("news_files.os.getenv") as mock_env,
        patch("news_files.time.sleep"),
    ):
      mock_env.side_effect = lambda k, default=None: {
          "PATH_LINKS": links_file,
          "PATH_PASTA_DESTINO": self.pasta_destino,
      }.get(k, default)

      extractor = NewsExtract()
      extractor.le_noticias()

      arquivo_gerado = os.path.join(self.pasta_destino, "news_sum_url_001.txt")
      self.assertTrue(os.path.exists(arquivo_gerado))
      with open(arquivo_gerado, "r", encoding="utf-8") as f:
        conteudo = f.read()

      self.assertIn("Texto extraido com sucesso da materia.", conteudo)


if __name__ == "__main__":
  unittest.main()
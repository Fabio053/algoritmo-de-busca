import re  # expressões regulares \b
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurando as palavras-chave
palavras_chave = ['via rondon', 'viarondon', 'via-rondon', 'Rodovia Marechal Rondon', 'sp-300', 'sp300', 'sp 300']

# Lista de sites adicionais para pesquisa
SITES_ADICIONAIS = ['site:g1.globo.com',
                    'site:thmais.com.br', 
                    'site:018news.com.br', 
                    'site:lr1.com.br', 
                    'site:sampi.net.br',
                    'site:investe.sp.gov.br',
                    'site:sbtinterior.com',
                    ]

# Lista de palavras indesejadas
palavras_indesejadas = ['futebol', 'samba', 'celebridades', 'entretenimento', 'fofoca', 'esporte', 'idoso', 'agredido', 'coma', 'ead', 'nia']

# Função para buscar notícias no Google
def busca_noticias(palavra_chave, data_inicio, data_fim):
    options = Options()

    # Remover o modo headless para testar o navegador com interface gráfica
    # options.add_argument("--headless")  # Comente ou remova esta linha para ver o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    data_inicio_formato = data_inicio.strftime('%Y-%m-%d')
    data_fim_formato = data_fim.strftime('%Y-%m-%d')

    sites_query = " OR ".join(SITES_ADICIONAIS)
    url = f'https://www.google.com/search?q={palavra_chave}+after:{data_inicio_formato}+before:{data_fim_formato}+{sites_query}&hl=pt'

    print(f"Buscando URL: {url}")
    driver.get(url)

    # Adicionando intervalo de tempo aleatório (2 a 5 segundos) antes de finalizar a busca
    time.sleep(random.uniform(2, 5))  # Pausa aleatória entre 2 e 5 segundos

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
        )
    except Exception as e:
        driver.quit()  # Fechar o navegador em caso de erro
        print(f"Erro ao buscar notícias para '{palavra_chave}': {str(e)}")
        return []

    noticias = []
    resultados = driver.find_elements(By.CSS_SELECTOR, 'div.g')

    if not resultados:
        print(f"Nenhum resultado encontrado para '{palavra_chave}'.")
        driver.quit()
        return []

    for result in resultados:
        try:
            titulo_element = result.find_element(By.TAG_NAME, 'h3')

            try:
                descricao_element = result.find_element(By.CSS_SELECTOR, 'div.IsZvec')
                descricao = descricao_element.text.lower()
            except Exception:
                descricao = ''

            link_element = result.find_element(By.TAG_NAME, 'a')

            if titulo_element and link_element:
                titulo = titulo_element.text.lower()
                link = link_element.get_attribute('href')

                # Ajuste na verificação de palavras-chave
                if any(palavra_chave.lower() in titulo or palavra_chave.lower() in descricao for palavra_chave in palavras_chave):
                    if not any(re.search(rf"\b{indesejada}\b", titulo) or re.search(rf"\b{indesejada}\b", descricao) for indesejada in palavras_indesejadas):
                        if link and "google" not in link:
                            print(f"Encontrou notícia: {titulo}")
                            noticias.append({"Título": titulo_element.text, "Link": link})
        except Exception as e:
            print(f"Erro ao processar o resultado: {str(e)}")
            continue
    
    # Adicionando intervalo de tempo aleatório (2 a 5 segundos) antes de finalizar a busca
    time.sleep(random.uniform(2, 5))  # Pausa aleatória entre 2 e 5 segundos

    driver.quit()
    return noticias


# Calculando as datas padrão (7 dias antes e 1 dia depois de hoje)
hoje = datetime.today()
data_inicio_default = hoje - timedelta(days=7)
data_fim_default = hoje + timedelta(days=1)

# Coletando datas
data_inicio = input(f"Data de Início (formato AAAA-MM-DD, padrão {data_inicio_default.strftime('%Y-%m-%d')}): ")
data_fim = input(f"Data de Fim (formato AAAA-MM-DD, padrão {data_fim_default.strftime('%Y-%m-%d')}): ")
data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d') if data_inicio else data_inicio_default
data_fim = datetime.strptime(data_fim, '%Y-%m-%d') if data_fim else data_fim_default

# Buscando notícias
dados = []
for palavra in palavras_chave:
    noticias = busca_noticias(palavra, data_inicio, data_fim)
    dados.extend(noticias)

# Salvando em um arquivo Excel
if dados:
    df = pd.DataFrame(dados)
    nome_arquivo = f"noticias_{hoje.strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')
    print(f"Arquivo salvo com sucesso: {nome_arquivo}")
else:
    print("Nenhuma notícia encontrada.")

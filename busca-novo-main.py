import re #expressões regulaer \b
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# Configurando as palavras-chave
palavras_chave = [
    'safra', 'madeira', 'celulose', 'bracell',
    'exportação', 'hidrovia', 'ferrovia', 'custo de frete',
    'eldorado Mato Grosso do Sul', 'suzano Três Lagoas', 'rota celulose',
    'ribas do rio pardo suzano', 'terminal intermodal', 'hidrovia tiete',
    'eucalipto', 'hexatrem', 'transporte de madeira', 'grãos', 'graneleiros',
    'preço combustível'
]

# Lista de sites adicionais para pesquisa
SITES_ADICIONAIS = [
    'site:portalcelulose.com.br',
    'site:portosenavios.com.br',
    'site:clickpetroleoegas.com.br',
    'site:g1.globo.com',
]

# Lista de palavras indesejadas
palavras_indesejadas = [
    'futebol', 'celebridades', 'entretenimento', 'fofoca', 'esporte', 'atropelado', 'idoso', 'suspeito', 'sobrevive', 'agredido',
    'coma', 
]

# Função para buscar notícias no Google
def busca_noticias(palavra_chave, data_inicio, data_fim):
    options = Options()
    options.add_argument("--headless")  # Executa o navegador em segundo plano
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    data_inicio_formato = data_inicio.strftime('%Y-%m-%d')
    data_fim_formato = data_fim.strftime('%Y-%m-%d')

    sites_query = " OR ".join(SITES_ADICIONAIS)
    url = f'https://www.google.com/search?q={palavra_chave}+notícias+after:{data_inicio_formato}+before:{data_fim_formato}+{sites_query}&hl=pt'
    
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(
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
            
            # Verificando se a descrição está presente, adicionando try-except
            try:
                descricao_element = result.find_element(By.CSS_SELECTOR, 'div.IsZvec')
                descricao = descricao_element.text.lower()
            except Exception:
                descricao = ''

            link_element = result.find_element(By.TAG_NAME, 'a')

            if titulo_element and link_element:
                titulo = titulo_element.text.lower()
                link = link_element.get_attribute('href')

                # Verificando se a palavra-chave está presente no título ou na descrição
                if any(re.search(rf"\b{palavra_chave.lower()}\b", titulo) or re.search(rf"\b{palavra_chave.lower()}\b", descricao) for palavra_chave in palavras_chave):

                    # Filtrando notícias com palavras indesejadas
                    if not any(re.search(rf"\b{indesejada}\b", titulo) or re.search(rf"\b{indesejada}\b", descricao) for indesejada in palavras_indesejadas):
                        if link and "google" not in link:
                            noticias.append({"Título": titulo_element.text, "Link": link})
        except Exception as e:
            print(f"Erro ao processar o resultado: {str(e)}")
            continue

    driver.quit()
    return noticias

# Calculando as datas padrão (2 dias antes e 1 dia depois de hoje)
hoje = datetime.today()
data_inicio_default = hoje - timedelta(days=2)
data_fim_default = hoje + timedelta(days=1)

# Coletando palavras-chave e datas
nova_palavra = input("Adicione uma nova palavra-chave (opcional): ").strip()
if nova_palavra:
    palavras_chave.append(nova_palavra)

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
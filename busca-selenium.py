import streamlit as st
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
        st.error(f"Erro ao buscar notícias para '{palavra_chave}': {str(e)}")
        return []

    noticias = []
    resultados = driver.find_elements(By.CSS_SELECTOR, 'div.g')

    if not resultados:
        st.warning(f"Nenhum resultado encontrado para '{palavra_chave}'.")
        driver.quit()
        return []

    for result in resultados:
        try:
            titulo_element = result.find_element(By.TAG_NAME, 'h3')
            link_element = result.find_element(By.TAG_NAME, 'a')

            if titulo_element and link_element:
                titulo = titulo_element.text
                link = link_element.get_attribute('href')

                # Verificação das palavras indesejadas
                if not any(palavra in titulo.lower() for palavra in palavras_indesejadas):
                    if link and "google" not in link:
                        noticias.append({"Título": titulo, "Link": link})
        except Exception as e:
            st.error(f"Erro ao processar o resultado: {str(e)}")
            continue

    driver.quit()
    return noticias

# Calculando as datas padrão (2 dias antes e 1 dia depois de hoje)
hoje = datetime.today()
data_inicio_default = hoje - timedelta(days=2)
data_fim_default = hoje + timedelta(days=1)

# Interface no Streamlit
st.title("Busca de Notícias")

palavras_selecionadas = st.multiselect("Selecione as palavras-chave:", palavras_chave)
nova_palavra = st.text_input("Adicione uma nova palavra-chave (opcional):")
data_inicio = st.date_input("Data de Início", data_inicio_default)
data_fim = st.date_input("Data de Fim", data_fim_default)

if st.button("Buscar Notícias"):
    if nova_palavra:
        palavras_selecionadas.append(nova_palavra)

    if palavras_selecionadas:
        dados = []
        for palavra in palavras_selecionadas:
            noticias = busca_noticias(palavra, data_inicio, data_fim)
            dados.extend(noticias)

        if dados:
            df = pd.DataFrame(dados)
            for index, row in df.iterrows():
                st.markdown(f"- **{row['Título']}**: [Link]({row['Link']})")
        else:
            st.write("Nenhuma notícia encontrada.")
    else:
        st.warning("Por favor, selecione pelo menos uma palavra-chave.")

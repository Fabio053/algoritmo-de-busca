from flask import Flask, render_template, request
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Configurando as palavras-chave
palavras_chave = [
    'safra', 'madeira', 'celulose', 'bracell',
    'exportação', 'safra', 'suzano', 'hidrovia', 'ferrovia', 
    'Combustível', 'custo de frete', 'eldorado Mato Grosso do Sul', 
    'rota celulose', 'ribas do rio pardo suzano', 
    'terminal intermodal pederneiras', 'hidrovia tiete', 
    'eldorado santos', 'eucalipto', 'caminhoes', 
    'hexatrens', 'rodovia'
]

# Lista de sites adicionais para pesquisa
SITES_ADICIONAIS = [
    'site:portalcelulose.com.br',
    'site:portosenavios.com.br',
    'site:clickpetroleoegas.com.br',
    'site:g1.globo.com',
]

# Função para buscar notícias no Google
def busca_noticias(palavra_chave, data_inicio, data_fim):
    options = Options()
    options.add_argument("--headless")  # Executa o navegador em segundo plano
    options.add_argument("--no-sandbox")  # Necessário em alguns ambientes
    options.add_argument("--disable-dev-shm-usage")  # Necessário em alguns ambientes

    chromedriver_autoinstaller.install()  # Isso tenta instalar a versão correta do ChromeDriver

    driver = webdriver.Chrome(service=Service(), options=options)

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
        return {"error": f"Erro ao buscar notícias para '{palavra_chave}': {str(e)}"}

    noticias = []
    resultados = driver.find_elements(By.CSS_SELECTOR, 'div.g')

    if not resultados:
        driver.quit()
        return {"warning": f"Nenhum resultado encontrado para '{palavra_chave}'."}

    for result in resultados:
        try:
            titulo_element = result.find_element(By.TAG_NAME, 'h3')
            link_element = result.find_element(By.TAG_NAME, 'a')

            if titulo_element and link_element:
                titulo = titulo_element.text
                link = link_element.get_attribute('href')

                if link and "google" not in link:
                    noticias.append({"Título": titulo, "Link": link})
        except Exception as e:
            continue

    driver.quit()
    return noticias

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        palavras_selecionadas = request.form.getlist('palavras')
        nova_palavra = request.form.get('nova_palavra', '')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        if nova_palavra:
            palavras_selecionadas.append(nova_palavra)

        if palavras_selecionadas and data_inicio and data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            dados = []

            for palavra in palavras_selecionadas:
                noticias = busca_noticias(palavra, data_inicio, data_fim)
                if isinstance(noticias, dict) and "error" in noticias:
                    return render_template('index.html', palavras=palavras_chave, mensagens=[noticias["error"]])
                dados.extend(noticias)

            return render_template('index.html', palavras=palavras_chave, dados=dados)

    return render_template('index.html', palavras=palavras_chave, dados=[])

if __name__ == '__main__':
    app.run(debug=True)

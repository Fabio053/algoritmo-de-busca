import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configurando o Selenium para usar o ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa o navegador em segundo plano (sem interface)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Lista de palavras-chave incluindo os estados São Paulo e Mato Grosso do Sul
palavras_chave = [
    'safra São Paulo', 'madeira São Paulo', 'celulose São Paulo', 'bracell São Paulo', 'exportação São Paulo', 'interior São Paulo',
    'safra Mato Grosso do Sul', 'madeira Mato Grosso do Sul', 'celulose Mato Grosso do Sul', 
    'bracell Mato Grosso do Sul', 'suzano Mato Grosso do Sul', 'exportação Mato Grosso do Sul', 
    'hidrovia São Paulo', 'ferrovia São Paulo', 'hidrovia Mato Grosso', 'ferrovia Mato Grosso Sul', 'Combustível São Paulo', 'Combustível Mato Grosso do Sul',
    'custo de frete', 'eldorado Mato Grosso do Sul', 'suzano Três Lagoas', 'rota celulose'
]

# Função para buscar notícias no Google
def busca_noticias(palavra_chave):
    # Montando a URL de busca no Google
    url = f'https://www.google.com/search?q={palavra_chave}+notícias&hl=pt'
    driver.get(url)
    time.sleep(2)  # Espera 2 segundos para a página carregar completamente
    
    # Coletando os links das notícias
    links = []
    resultados = driver.find_elements(By.XPATH, '//a')
    
    for result in resultados:
        link = result.get_attribute('href')
        if link and "google" not in link:
            links.append(link)
    
    return links

# Função para criar um link clicável no Excel
def criar_link_clicavel(url):
    return f'=HYPERLINK("{url}", "{url}")'

# Coletando links para todas as palavras-chave
dados = []
for palavra in palavras_chave:
    links = busca_noticias(palavra)
    for link in links:
        dados.append([palavra, criar_link_clicavel(link)])

# Criando DataFrame e salvando em Excel
df = pd.DataFrame(dados, columns=['Palavra Chave', 'Link Clicável'])
df.to_excel('noticias_links_selenium.xlsx', index=False, engine='openpyxl')

# Fechando o navegador
driver.quit()

print("Planilha gerada com sucesso!")

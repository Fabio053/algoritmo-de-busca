#%%
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#%%
# Configurando o Selenium para usar o ChromeDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa o navegador em segundo plano (sem interface)
options.add_argument("--disable-gpu")  # Desativa o uso de GPU para evitar erros
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Lista de palavras-chave fornecidas
palavras_chave = [
    'Viarondon', 'V.C.R', 'via rondon', 
    'AGÊNCIA REGULADORA DE SERVIÇOS PÚBLICOS DELEGADOS DE TRANSPORTE DO ESTADO DE SÃO PAULO',
    '038.130', '029.934', '023.178', '021.00001454/2023-08', 'ARTESP'
]

# Função para buscar notícias no site da Imprensa Oficial
def busca_imprensa_oficial(palavra_chave):
    url = 'https://www.imprensaoficial.com.br/'
    driver.get(url)
    
    try:
        # Espera até que o campo de busca esteja presente e visível
        campo_busca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'ctl00$corpo$txtPalavra'))
        )
        
        campo_busca.clear()
        campo_busca.send_keys(palavra_chave)
        campo_busca.send_keys(Keys.RETURN)
        time.sleep(10)  # Aguardar carregamento dos resultados

        # Coletando os links
        links = []
        resultados = driver.find_elements(By.XPATH, '//a[@class="link-result"]')  # Verificar o seletor correto

        for resultado in resultados:
            link = resultado.get_attribute('href')
            if link:
                links.append(link)
                
        return links

    except TimeoutException:
        print(f"Elemento de busca não encontrado para a palavra: {palavra_chave}")
        return []

# Função para buscar notícias no site DOE
def busca_doe(palavra_chave):
    url = 'https://www.doe.sp.gov.br/busca-avancada'
    driver.get(url)
    
    try:
        # Espera até que o campo de busca esteja presente e visível
        campo_busca = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'busca'))  # Verifique se 'busca' é o nome correto
        )
        
        campo_busca.clear()
        campo_busca.send_keys(palavra_chave)
        campo_busca.send_keys(Keys.RETURN)
        time.sleep(10)  # Aguardar carregamento dos resultados
        
        # Coletando os links
        links = []
        resultados = driver.find_elements(By.XPATH, '//a[@class="link-result"]')  # Verifique se este é o seletor correto

        for resultado in resultados:
            link = resultado.get_attribute('href')
            if link:
                links.append(link)
        
        return links

    except TimeoutException:
        print(f"Elemento de busca não encontrado para a palavra: {palavra_chave}")
        return []

# Função para criar um link clicável no Excel
def criar_link_clicavel(url):
    return f'=HYPERLINK("{url}", "{url}")'
#%%
# Coletando links para todas as palavras-chave
dados = []
for palavra in palavras_chave:
    # Imprensa Oficial
    links_imprensa = busca_imprensa_oficial(palavra)
    for link in links_imprensa:
        dados.append([palavra, criar_link_clicavel(link), 'Imprensa Oficial'])
    
    # DOE
    links_doe = busca_doe(palavra)
    for link in links_doe:
        dados.append([palavra, criar_link_clicavel(link), 'DOE'])
#%%
# Criando DataFrame e salvando em Excel
df = pd.DataFrame(dados, columns=['Palavra Chave', 'Link Clicável', 'Fonte'])
df.to_excel('resultados_imprensa_doe.xlsx', index=False, engine='openpyxl')

# Fechando o navegador
driver.quit()

print("Planilha gerada com sucesso!")

# %%

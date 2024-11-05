import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configurando as palavras-chave
palavras_chave = [
    'safra', 'madeira', 'celulose', 'bracell',
    'exportação', 'safra', 'suzano', 'hidrovia', 'ferrovia', 'Combustível', 'custo de frete',
    'eldorado Mato Grosso do Sul', 'rota celulose',
    'ribas do rio pardo suzano', 'terminal intermodal pederneiras', 'hidrovia tiete',
    'eldorado santos', 'eucalipto', 'caminhoes', 'hexatrens', 'rodovia'
]

# Função para buscar notícias no Google News
def busca_noticias(palavra_chave, data_inicio, data_fim):
    # Formatar as datas
    data_inicio_formato = data_inicio.strftime('%Y-%m-%d')
    data_fim_formato = data_fim.strftime('%Y-%m-%d')

    # Montar a URL da busca no Google News
    url = f"https://news.google.com/search?q={palavra_chave}+after:{data_inicio_formato}+before:{data_fim_formato}&hl=pt-BR&gl=BR"

    # Fazer a requisição HTTP
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Erro ao buscar notícias: {response.status_code}")
        return []

    # Analisar o conteúdo da página
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    
    # Selecionar artigos usando o seletor correto para Google News
    resultados = soup.find_all('article')

    for result in resultados:
        try:
            titulo_element = result.find('h3')
            link_element = result.find('a')

            if titulo_element and link_element:
                titulo = titulo_element.text
                link = link_element['href']

                # Ajustando o link caso ele seja relativo
                if link.startswith('.'):
                    link = 'https://news.google.com' + link[1:]

                noticias.append({"Título": titulo, "Link": link})
        except Exception as e:
            st.error(f"Erro ao processar o resultado: {str(e)}")
            continue

    return noticias

# Interface no Streamlit
st.title("Busca de Notícias")

palavras_selecionadas = st.multiselect("Selecione as palavras-chave:", palavras_chave)
nova_palavra = st.text_input("Adicione uma nova palavra-chave (opcional):")
data_inicio = st.date_input("Data de Início", pd.to_datetime("2024-01-01"))
data_fim = st.date_input("Data de Fim", pd.to_datetime("2024-12-31"))

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

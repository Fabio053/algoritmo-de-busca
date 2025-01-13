# Documentação do Script: Busca de Notícias e Salvamento em Excel

## Descrição

Este script realiza a busca de notícias no Google com base em palavras-chave fornecidas, em um intervalo de datas configurado pelo usuário, e salva os resultados em um arquivo Excel. Ele utiliza as bibliotecas Selenium para automação da navegação e Pandas para manipulação de dados e geração do arquivo Excel.

## Funcionalidades

Busca notícias em sites específicos, utilizando palavras-chave definidas.

Filtra resultados que contenham palavras indesejadas.

Permite a personalização das palavras-chave e intervalos de datas.

Gera um arquivo Excel com os títulos das notícias e seus respectivos links.

## Requisitos

### Pré-requisitos:

- Python 3.7 ou superior

    Instalar as dependências do projeto:

```pip install selenium pandas openpyxl webdriver-manager```

- Navegador e WebDriver:

    Google Chrome deve estar instalado.

    O script utiliza o WebDriver gerenciado automaticamente pelo webdriver-manager.

## Como Usar

1. Clone este repositório ou copie o script para seu ambiente local.

2. Execute o script no terminal ou em seu ambiente Python preferido.

3. Durante a execução, forneça os seguintes dados:

4. Opcionalmente, uma nova palavra-chave.

5. Datas de início e fim para a busca no formato AAAA-MM-DD. Caso não sejam fornecidas, será utilizado o intervalo padrão (últimos 2 dias até amanhã).

6. Após a execução, o arquivo Excel será gerado no mesmo diretório do script, com o nome no formato: noticias_YYYYMMDD_HHMMS.xlsx.

## Estrutura do Código

- Bibliotecas Importadas

    selenium: Para automação do navegador.

    pandas: Para manipulação de dados.

    datetime: Para cálculo de intervalos de datas.

    webdriver-manager: Para gerenciar o WebDriver do Chrome.

## Fluxo Principal

### Configuração inicial:

Define palavras-chave e sites para a busca.

Lista palavras indesejadas para filtro.

### Entrada do usuário:

Permite adicionar uma nova palavra-chave e configurar datas.

### Busca de notícias:

Automatiza a navegação no Google para coletar resultados.

Filtra os resultados com base em palavras indesejadas.

### Geração do arquivo Excel:

Salva os resultados em um arquivo Excel utilizando openpyxl.

## Exemplos de Uso

#### Exemplo 1: Busca Padrão

Sem adicionar nova palavra-chave.

Usando o intervalo padrão (últimos 2 dias até amanhã).

Resultado: Arquivo Excel com notícias relacionadas às palavras-chave predefinidas.

### Exemplo 2: Busca Personalizada

Adicionar nova palavra-chave: transporte ferroviário.

Intervalo de datas: 2025-01-01 a 2025-01-10.

Resultado: Arquivo Excel com notícias filtradas pelo intervalo e palavras-chave personalizadas.

## Observações

O script utiliza o Google como motor de busca. Dependendo da região e idioma, os resultados podem variar.

Verifique se o Google bloqueia requisições automáticas ao executar o script muitas vezes.

Possíveis Erros e Soluções

Erro de conexão com o WebDriver:

Certifique-se de que o Chrome está instalado e atualizado.

Atualize o webdriver-manager com o comando:

pip install --upgrade webdriver-manager

Resultados vazios:

Confirme que as palavras-chave fornecem resultados relevantes.

Verifique sua conexão com a internet.

Autor

Desenvolvido por Filipe GUidastri.

Entre em contato para dúvidas ou sugestões.
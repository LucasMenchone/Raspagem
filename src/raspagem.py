import requests
from bs4 import BeautifulSoup
import csv

arquivo_csv = '.\src\data\produtos.csv'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

produto = 'Pulverizador-Costal-Manual'

url = f'https://lista.mercadolivre.com.br/{produto}'

start = 1

def extrair_valores(texto):
    texto = texto.replace("R$", "").replace("% OFF", "").strip()
    texto = texto.replace(".", "").replace(",", ".")
    try:
        return f"{float(texto):.2f}"
    except ValueError:
        return "0.00"  


resultados = []

while True:
    url_final = url + '_Desde_' + str(start) + '_' + 'NoIndex_True'

    r = requests.get(url_final, headers=headers)

    site = BeautifulSoup(r.content, 'html.parser')

    anuncios = site.find_all('li', class_='ui-search-layout__item')
    for i in anuncios:
        resultados.append(i)
    
    if not anuncios:
        print('Sem mais itens.')
        break

    resultados_len = len(resultados)
    print(f'Anúncios encontrados: {str(resultados_len)}')
    start += 50

marcas, modelos, precos = [], [], []

for i in resultados:
    if not i.find('span', class_='poly-component__brand'):
        marcas.append('N/A')
    else:
        marcas.append(i.find('span', class_='poly-component__brand').get_text())

    modelos.append(i.find('h2', class_='poly-box poly-component__title').get_text())

    preco_element = i.find('div', class_='poly-price__current') 
    if preco_element:
        fraction_element = preco_element.find('span', class_='andes-money-amount__fraction')
        if fraction_element:
            preco = extrair_valores(fraction_element.get_text())
        else:
            preco = 0.0
    else:
        preco = 0.0  
    
    precos.append(preco)

with open(arquivo_csv, mode='w', newline='', encoding='utf-8-sig') as file:
    escritor_csv = csv.writer(file, delimiter=';')

    escritor_csv.writerow(['Marca', 'Modelo', 'Preço'])

    escritor_csv.writerows(zip(marcas, modelos, precos))
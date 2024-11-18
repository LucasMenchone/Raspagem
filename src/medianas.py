import pandas as pd
from fuzzywuzzy import process
from collections import defaultdict

def filtrar_produtos(file_path):
    """
    Filtra o arquivo 'produtos.csv', mantendo apenas registros cujo 'Modelo'
    contenha todas as palavras: 'pulverizador', 'costal' e 'manual'.
    Retorna um DataFrame filtrado.
    """
    produtos_df = pd.read_csv(file_path, delimiter=';', encoding='utf-8-sig')
    
    produtos_df['Modelo'] = produtos_df['Modelo'].str.upper()
    
    palavras_chave = ['PULVERIZADOR', 'COSTAL', 'MANUAL']
    filtro = produtos_df['Modelo'].apply(
        lambda x: all(palavra in x for palavra in palavras_chave)
    )
    
    return produtos_df[filtro]

file_path = '.\src\data\produtos.csv'

produtos_df = filtrar_produtos(file_path)

produtos_df['Marca'] = produtos_df['Marca'].str.upper()
produtos_df['Modelo'] = produtos_df['Modelo'].str.upper()

produtos_df.loc[
    (produtos_df['Marca'] == 'N/A') & produtos_df['Modelo'].str.contains('PULVERIZADOR'),
    'Marca'
] = 'NÃO DECLARADO'

produtos_df = produtos_df[~((produtos_df['Marca'] == 'N/A') & ~produtos_df['Modelo'].str.contains('PULVERIZADOR'))]

produtos_df['Preço'] = pd.to_numeric(produtos_df['Preço'])

produtos_df = produtos_df.dropna(subset=['Preço'])

agrupados = []
similarity_threshold = 90

for marca in produtos_df['Marca'].unique():
    
    modelos = produtos_df[produtos_df['Marca'] == marca]['Modelo'].unique()
    grupos = defaultdict(list)

    for modelo in modelos:
    
        match = process.extractOne(modelo, grupos.keys(), score_cutoff=similarity_threshold)
        if match:
            grupos[match[0]].append(modelo)
        else:
            grupos[modelo].append(modelo)

    modelo_para_grupo = {m: g for g, ms in grupos.items() for m in ms}

    marca_df = produtos_df[produtos_df['Marca'] == marca].copy()
    marca_df['Grupo_Modelo'] = marca_df['Modelo'].map(modelo_para_grupo)
    agrupados.append(marca_df)

produtos_agrupados_df = pd.concat(agrupados)

medianas_df = (
    produtos_agrupados_df.groupby(['Marca', 'Grupo_Modelo'])['Preço']
    .median()
    .round(2)
    .reset_index()
    .rename(columns={'Grupo_Modelo': 'Modelo', 'Preço': 'Mediana_Preço'})
)

output_path = '.\src\data\medianas.csv'
medianas_df.to_csv(output_path, sep=';', encoding='utf-8-sig', index=False)

print(f"Arquivo 'medianas.csv' gerado com sucesso no caminho: {output_path}")
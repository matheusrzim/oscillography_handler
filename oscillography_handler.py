import numpy as np
import pandas as pd
from scipy.io import loadmat
from pathlib import Path
import sys

# Parameters
hz = 60 #Hz System frequency
comtrade_pool = 1920 #Hz = 512us for each sample


# Function for creating readable oscilography
def create_osci(pth):
    aux = open(pth,'r')
    osci = aux.read()
    aux.close()
    osci1 = osci.split('\n') #dividido em linhas str
    osci2 = np.zeros((len(osci1)-1,(len(osci1[0].split(','))))) # initialize osci2 with necessary dimension
    for i in range(0,(len(osci1)-1)): # lines
        for t in range(0,(len(osci1[i].split(',')))): # columns
            osci2 [i][t] = float((osci1[i].split(','))[t])
    return osci2

# Defining the scrip path
pth = Path(__file__).parent / 'data'
files = []

# Loading files
for each_file in pth.iterdir():
    files.append(each_file)

dat = [files for files in pth.glob('*.dat')]
cfg = [files for files in pth.glob('*.cfg')]
mat = [files for files in pth.glob('*.mat')]

test = pd.DataFrame(create_osci(dat[0]))

test = test.iloc[:, 2:4]

print(test)
try:
    PASTA_ORIGEM = pth
    PASTA_SAIDA_CSV = pth / 'pasta_csv_convertida'

# --- 2. Criar pasta de destino se não existir ---
    PASTA_SAIDA_CSV.mkdir(parents=True, exist_ok=True)

# --- 3. Encontrar todos os arquivos .mat ---
    lista_arquivos_mat = list(PASTA_ORIGEM.glob('*.mat'))

    if not lista_arquivos_mat:
        print(f"Erro: Nenhum arquivo .mat encontrado em {PASTA_ORIGEM}")
        sys.exit() # Para o script se não encontrar nada

    caminho_arquivo_mat = lista_arquivos_mat[0]
    print(f"Processando arquivo: {caminho_arquivo_mat.name}")

    # --- 3. Carregar o arquivo .mat ---
    # O scipy.io.loadmat() lê o arquivo .mat e o retorna como um dicionário
    dados_mat = loadmat(caminho_arquivo_mat)

    # --- 4. Encontrar a variável de dados ---
    # Um .mat tem metadados (ex: '__header__'). 
    # Queremos a chave que NÃO é metadado.
    nome_da_variavel = [k for k in dados_mat.keys() if not k.startswith('__')][0]
    
    print(f"Variável encontrada dentro do .mat: '{nome_da_variavel}'")

    # Acessa os dados (que são um array)
    array_de_dados = dados_mat[nome_da_variavel]

    # --- 5. Transformar em DataFrame ---
    # Como você disse que é apenas uma coluna, criamos o DF
    # e damos à coluna o nome da variável que encontramos
    df = pd.DataFrame(array_de_dados, columns=[nome_da_variavel])

    print("DataFrame criado com sucesso:")
    print(df.head()) # Mostra as 5 primeiras linhas

    # --- 6. Salvar como .csv ---
    # Pegamos o nome do arquivo original (ex: 'dados.mat' -> 'dados')
    nome_base = caminho_arquivo_mat.stem
    
    # Criamos o caminho de saída (ex: 'arquivos_csv/dados.csv')
    caminho_arquivo_csv = PASTA_SAIDA_CSV / f"{nome_base}.csv"

    # Salva o arquivo .csv, sem incluir o índice do pandas
    df.to_csv(caminho_arquivo_csv, index=False)

    print(f"\nArquivo salvo com sucesso em: {caminho_arquivo_csv}")
    print(lista_arquivos_mat)

except FileNotFoundError:
    print(f"Erro: A pasta de entrada não foi encontrada: {PASTA_ORIGEM}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
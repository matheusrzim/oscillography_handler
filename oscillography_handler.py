import numpy as np
import pandas as pd
from scipy.io import loadmat
from pathlib import Path
import sys

# Parameters
hz = 60 #Hz System frequency
comtrade_sample = 1920 #Hz = 512us for each sample

def comtrade_to_csv(pth):
    aux = open(pth,'r')
    osci = aux.read()
    aux.close()
    osci1 = osci.split('\n') #dividido em linhas str
    osci2 = np.zeros((len(osci1)-1,(len(osci1[0].split(','))))) # initialize osci2 with necessary dimension
    for i in range(0,(len(osci1)-1)): # lines
        for t in range(0,(len(osci1[i].split(',')))): # columns
            osci2 [i][t] = float((osci1[i].split(','))[t])
    return osci2

def mat_to_csv(pth):
    try:
        root_pth = pth
        csv_folder = pth / 'mat_to_csv'
        csv_folder.mkdir(parents=True, exist_ok=True)
        list_mat = list(root_pth.glob('*.mat'))

        if not list_mat:
            print(f"Error: None .mat found at {root_pth}")
            sys.exit() # Stop script

        pth_mat = list_mat[0]
        print(f"Processando arquivo: {pth_mat.name}")

        for file in list_mat:
            mat_data = loadmat(file)
            key = [k for k in mat_data.keys() if not k.startswith('__')][0] # A .mat file has metadata, gets only the key that is not metadata
            df = pd.DataFrame(mat_data[key], columns=[key])
            file_name = file.stem
            csv_path = csv_folder / f"{file_name}.csv"
            df.to_csv(csv_path, index=False)

        print('\nFiles saved successfully at:', csv_folder)
    except FileNotFoundError:
        print(f"Error: The given folder was not found: {root_pth}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Defining the scrip path
pth = Path(__file__).parent / 'data'
files = []

# Loading files
for each_file in pth.iterdir():
    files.append(each_file)

dat = [files for files in pth.glob('*.dat')]
cfg = [files for files in pth.glob('*.cfg')]
mat = [files for files in pth.glob('*.mat')]

test = pd.DataFrame(comtrade_to_csv(dat[0]))

mat_to_csv(pth) # Creates all .csv from .mat files

test = test.iloc[:, 2:4]


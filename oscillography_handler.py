import numpy as np
import pandas as pd
from pathlib import Path

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

print(test)

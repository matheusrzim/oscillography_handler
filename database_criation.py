import numpy as np
import glob

n_fases = 3 # número de fases (3 para oscilografia trifásica)
n_train = 63
n_teste = 36
f_amostragem = 15360 # [amostras/s]
f_requerida = 4000 # [amostras/s]
razao_amostragem = round(f_amostragem/f_requerida)
t_pre_falta = 1 # [segundos]
t_max = 4 # [segundos] tempo maximo observado para identificar as faltas
amostras = int(f_amostragem*(t_pre_falta + t_max))

def criar_pacote(caminho):
    arquivo = open(caminho,'r')
    osci = arquivo.read()
    arquivo.close()
    osci1 = osci.split('\n') #dividido em linhas str
    osci2 = np.zeros((len(osci1)-1,(len(osci1[0].split(','))))) #inicializa osci2 com o numero de linhas e colunas necessarios
    for i in range(0,(len(osci1)-1)):
        #indice das linhas
        for t in range(0,(len(osci1[i].split(',')))):
            #indice das colunas
            osci2 [i][t] = np.float((osci1[i].split(','))[t])
    return osci2

def criar_base_nova(caminho):
    caminho = r'C:/User/' + caminho
    caminho = (caminho.replace('\\','/')+'**/*.dat')
    # Inicia os valores que serão utilizados
    entrada_train = np.zeros((n_train,amostras,n_fases))
    saida_train = np.zeros((n_train,1))
    entrada_test = np.zeros((n_teste,amostras,n_fases))
    saida_test = np.zeros((n_teste,1))
    x = []
    y = []
    count_test = 0
    count_train = 0
    for each_file in glob.glob('C:/Users/*.dat', recursive=True):
        x.append(each_file)
    for each_file in glob.glob('C:/Users/*.dat.csv', recursive=True):
        y.append(each_file)
    for i in range(0,(len(x))):
    #for i in range(0,20): #para pegar apenas a primeira pasta
        x[i] = x[i].replace('\\','/')
        #print(x[i])
        osci = criar_pacote(x[i])
        #print(np.shape(osci))
        #print(len(osci))
        if 'test' in x[i]:
            for j in range(0,(len(osci))):
                if j < amostras:
                    for k in range(0,n_fases):
                        entrada_test [count_test][j][k] = osci[j][k+2]    
                else:
                    break
            count_test +=  1
        elif 'train' in x[i]:
            for j in range(0,(len(osci))):
                if j < amostras:
                    for k in range(0,n_fases):
                        entrada_train [count_train][j][k] = osci[j][k+2]
                else:
                    break
            count_train +=  1
    for i in range(0,(len(y))):
        y[i] = y[i].replace('\\','/')
        print(i)
        if 'test' in y[i]:
            arquivo = open(y[i],'r',encoding='utf-8-sig')
            aux = arquivo.read()
            arquivo.close()
            for j in range(0,n_teste):
                saida_test[j] = aux.split('\n')[j]
        elif 'train' in y[i]:
            arquivo = open(y[i],'r',encoding='utf-8-sig')
            aux = arquivo.read()
            arquivo.close()
            for j in range(0,n_train):
                saida_train[j] = aux.split('\n')[j]
    
    # ## Remodela para 2D            
    # remodelar_test = np.zeros((108,amostras)) # para 20 conjuntos com fases A, B e C
    # remodelar_train = np.zeros((189,amostras)) # para 40 conjuntos com fases A, B e C
    # for i in range(36): # primeiro o teste
    #     for j in range(3):
    #         for k in range(amostras):
    #             remodelar_test[(3*i+j)] [k] = entrada_test[i][k][j+2]
    # for i in range(63):
    #     for j in range(3):
    #         for k in range(amostras):
    #             remodelar_train[(3*i+j)] [k] = entrada_train[i][k][j+2]
    # # entrada_test = remodelar_test
    # # entrada_train = remodelar_train

    ## Para diminuir o número de amostras (soma ('razao_amostragem' número de amostras) e divide por 'razao_amostragem')  
    
    remodelar_test = np.zeros((len(entrada_test),(int(len(entrada_test[0])/razao_amostragem)),(len(entrada_test[0][0]))))
    remodelar_train = np.zeros((len(entrada_train),(int(len(entrada_train[0])/razao_amostragem)),(len(entrada_train[0][0]))))
    for i in range(0,len(remodelar_test)):
        for j in range(0,len(remodelar_test[0])):
            for k in range(0,len(remodelar_test[0][0])):
                remodelar_test[i][j][k] = (entrada_test[i][j*4][k] + entrada_test[i][j*4 + 1][k] + entrada_test[i][j*4 + 2][k] + entrada_test[i][j*4 + 3][k])/razao_amostragem
    for i in range(0,len(remodelar_train)):
        for j in range(0,len(remodelar_train[0])):
            for k in range(0,len(remodelar_train[0][0])):
                remodelar_train[i][j][k] = (entrada_train[i][j*4][k] + entrada_train[i][j*4 + 1][k] + entrada_train[i][j*4 + 2][k] + entrada_train[i][j*4 + 3][k])/razao_amostragem
    entrada_test = remodelar_test
    entrada_train = remodelar_train
    
    # ## Para positivar todos os valores

    for i in range(0,len(entrada_test)):
        for j in range(0,len(entrada_test[0])):
            entrada_test[i][j] = entrada_test[i][j] + 100000 #100000 é o valor máximo dentro do arquivo COMTRADE
    for i in range(0,len(entrada_train)):
        for j in range(0,len(entrada_train[0])):
            entrada_train[i][j] = entrada_train[i][j] + 100000

    ##Para normalizar (x-xmin/xmax-xmin) todos os valores

    x_test_min = entrada_test.min()
    x_test_max = entrada_test.max()
    x_train_min = entrada_train.min()
    x_train_max = entrada_train.max()

    for i in range(0,len(entrada_test)):
        for j in range(0,len(entrada_test[0])):
            for k in range(0,len(entrada_test[0][0])):
                entrada_test[i][j][k] = (entrada_test[i][j][k] - x_test_min)/(x_test_max - x_test_min)
    for i in range(0,len(entrada_train)):
        for j in range(0,len(entrada_train[0])):
            for k in range(0,len(entrada_train[0][0])):
                entrada_train[i][j][k] = (entrada_train[i][j][k] - x_train_min)/(x_train_max - x_train_min)
    
    dados = ((entrada_test,saida_test),(entrada_train,saida_train))
    np.save('dados_4kHz_3D_5s_norm_pos',dados)
    return dados


(X_train, y_train), (X_test, y_test) = criar_base_nova('C:/Users')

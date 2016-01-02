#-*- coding: utf-8 -*-

from pyfann import libfann
from math import sqrt
from config import qntNeuroniosEntrada, qntNeuroniosSaida, logFile

# Genes de um cromossomo
qntCamadasOcultas = [ 1, 2 ]
taxaAprendizado   = [ x*0.1 for x in (range(1,9)) ]
momentum          = [ x*0.1 for x in (range(1,9)) ]
lrdecay           = [ x*0.1 for x in (range(1,9)) ]
funcoesTreino     = [ libfann.TRAIN_INCREMENTAL, libfann.TRAIN_QUICKPROP,
                      libfann.TRAIN_RPROP, libfann.TRAIN_BATCH ]
funcoesAtivacao   = [ libfann.SIGMOID, libfann.SIGMOID_SYMMETRIC,
                      libfann.SIGMOID_STEPWISE, libfann.SIGMOID_SYMMETRIC_STEPWISE,
                      libfann.LINEAR, libfann.LINEAR_PIECE,
                      libfann.LINEAR_PIECE_SYMMETRIC, libfann.THRESHOLD,
                      libfann.THRESHOLD_SYMMETRIC, libfann.GAUSSIAN,
                      libfann.GAUSSIAN_STEPWISE, libfann.GAUSSIAN_SYMMETRIC,
                      libfann.ELLIOT, libfann.ELLIOT_SYMMETRIC,
                      libfann.COS_SYMMETRIC, libfann.SIN_SYMMETRIC ]
neuroniosOcultos  = [ 5, 8, 10, 12, 15, 50, 80, 100, 200, 300,
                      int(sqrt(qntNeuroniosEntrada+qntNeuroniosSaida)*2),
                      int((qntNeuroniosEntrada+qntNeuroniosSaida)/2) ]
epocasTreinamento = [ 100, 200, 300 ]

''' Conteúdo do vetor tipoGenes:
    [0] Quantidade de camadas ocultas da RNA
    [1] Função de ativação da(s) camada(s) oculta(s)
    [2] Função de ativação da camada de saída
    [3] Quantidade de Neurônios Ocultos
    [4] Algoritmo de Aprendizado
    [5] Taxa de Aprendizado
    [6] Momentum
    [7] Lr Decay
    [8] Quantidade de épocas a treinar
'''
# Matriz com os tipos de genes
tipoGenes = [ qntCamadasOcultas, funcoesAtivacao, funcoesAtivacao, neuroniosOcultos,
              funcoesTreino,  taxaAprendizado, momentum, lrdecay, epocasTreinamento ]

#-------------------------------------------------------------------------------------------#

def avaliacaoRNA(cromo):
    '''
    Função responsável pela avaliação da RNA
    '''
    resultado = ''
    valorRet  = 999.0

    c = cromo.getCromossomo()

    try:
        from os import popen
        resultado = popen(
                           "./Avaliador_Fann %s %s %s %s %s %s %s %s %s" % \
                            (c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8])
                          ).readlines()
      
        strResultado = resultado[-1]
        if strResultado.find('Resultado') <> -1:
            valorRet = float(strResultado.split()[-1])
        else:
            valorRet = 999.0
    except:
        resultado = ["Resultado: 999.0 (ERRO: Combinação de rede errada)\n"]
        valorRet = 999.0

    log = open( logFile , "a" )
    log.write("Cromossomo %s\n"%c)
    for i in resultado: log.write(i)
    log.write("_"*50+'\n')
    log.close()
    return valorRet

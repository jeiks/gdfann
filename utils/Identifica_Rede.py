#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Jacson RC Silva <jacsonrcsilva@gmail.com>
'''

from pyfann import libfann
from sys import argv, exit

if len(argv) <> 10:
    print 'Use: %s gene1 gene2 gene3 gene4 gene5 gene6 gene7 gene8 gene9' % (argv[0])
    exit(1)

entrada = map( lambda x: x.replace(',','').replace('[','').replace(']',''), argv[1:] )

def getCamada(num):
    num = int(num)
    if   num == libfann.SIGMOID:
        return 'SIGMOID'
    elif num == libfann.SIGMOID_SYMMETRIC:
        return 'SIGMOID_SYMMETRIC'
    elif num == libfann.SIGMOID_STEPWISE:
        return 'SIGMOID_STEPWISE'
    elif num == libfann.SIGMOID_SYMMETRIC_STEPWISE:
        return 'SIGMOID_SYMMETRIC_STEPWISE'
    elif num == libfann.LINEAR:
        return 'LINEAR'
    elif num == libfann.LINEAR_PIECE:
        return 'LINEAR_PIECE'
    elif num == libfann.LINEAR_PIECE_SYMMETRIC:
        return 'LINEAR_PIECE_SYMMETRIC'
    elif num == libfann.THRESHOLD:
        return 'THRESHOLD'
    elif num == libfann.THRESHOLD_SYMMETRIC:
        return 'THRESHOLD_SYMMETRIC'
    elif num == libfann.GAUSSIAN:
        return 'GAUSSIAN'
    elif num == libfann.GAUSSIAN_STEPWISE:
        return 'GAUSSIAN_STEPWISE'
    elif num == libfann.GAUSSIAN_SYMMETRIC:
        return 'GAUSSIAN_SYMMETRIC'
    elif num == libfann.ELLIOT:
        return 'ELLIOT'
    elif num == libfann.ELLIOT_SYMMETRIC:
        return 'ELLIOT_SYMMETRIC'
    elif num == libfann.COS_SYMMETRIC:
        return 'COS_SYMMETRIC'
    elif num == libfann.SIN_SYMMETRIC:
        return 'SIN_SYMMETRIC'

def getAprendizado(num):
    num = int(num)
    if   num == libfann.TRAIN_INCREMENTAL:
        return 'TRAIN_INCREMENTAL'
    elif num == libfann.TRAIN_QUICKPROP:
        return 'TRAIN_QUICKPROP'
    elif num == libfann.TRAIN_RPROP:
        return 'TRAIN_RPROP'
    elif num == libfann.TRAIN_BATCH:
        return 'TRAIN_BATCH'

print 'Quantidade de Camadas ocultas:   ', entrada[0]
print 'Função da camada oculta:         ', getCamada(entrada[1])
print 'Função da camada de saída:       ', getCamada(entrada[2])
if int(entrada[0]) == 1:
    print 'Quantidade de Neurônios Ocultos: ', entrada[3]
else:
    print 'Neurônios Ocultos'
    aux = int(entrada[3])*2
    for i in range(int(entrada[0])):
        print '   %dª Camada Oculta:             %d' % (i+1, aux/2)
        aux = aux / 2
print 'Algoritmo de Aprendizado:        ', getAprendizado(entrada[4])
print 'Learning Rate:                   ', entrada[5]
print 'Momentum:                        ', entrada[6]
print 'Lr Decay:                        ', entrada[7]
print 'Máximo de épocas de treino:      ', entrada[8]

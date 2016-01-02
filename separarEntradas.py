#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit
from random import randint
from config import qntNeuroniosEntrada, qntNeuroniosSaida, nomeArqTreino, nomeArqValidacao, nomeArqTeste, porcTreino

def printMsg(msg):
    print "Sep.Entradas:: \033[36;2m%s\033[0m" % msg

def printError(msg, exitNumber):
    print "ERROR (Sep.Entradas):: %s" % msg
    exit(exitNumber)

if len(argv) != 2:
    printError("\nUse: %s arquivoComTodosOsPadroes" % argv[0], 1)

try:    linhas = open( argv[1] ).readlines()
except: printError("O arquivo `%s' não pode ser aberto!" % argv[1], 2)

if len(linhas[0]) <> len(linhas[1]):
    linhas = linhas[1:]

printMsg("Removendo os padrões repetidos...")
linhas = list( set( linhas ) )

if len(linhas[0].split()) <> qntNeuroniosEntrada+qntNeuroniosSaida:
    printError("O arquivo de padrões não possui a quantidade correta de entradas e saídas.", 3)

printMsg("Aleatorizando...")
from random import shuffle
shuffle(linhas)

qntTodoTreino = int( porcTreino * len( linhas ) )
qntTreino     = int( porcTreino * qntTodoTreino )
qntValidacao  = qntTodoTreino - qntTreino
qntTestes     = len(linhas) - qntTodoTreino

printMsg("Separando padrões de treino, de validação e de testes...")

padroesTreino    = linhas[:qntTreino]
padroesValicadao = linhas[qntTreino:(qntValidacao+qntTreino)]
padroesTeste     = linhas[(qntValidacao+qntTreino):]

printMsg("Gravando padrões de treino (%d), de validação (%d) e de testes (%d)..." % (len(padroesTreino), len(padroesValicadao), len(padroesTeste)))

try:
    arq = open( nomeArqTreino.split('/')[-1] , 'w' )
    tam = len(padroesTreino)
    arq.write('%d %d %d\n' % (tam, qntNeuroniosEntrada, qntNeuroniosSaida) )
    arq.writelines( padroesTreino )
    arq.close()
except:
    printError("Impossível gravar os padrões de treino em `%s'" % nomeArqTreino, 4)

try:
    arq = open( nomeArqValidacao.split('/')[-1] , 'w' )
    tam = len(padroesValicadao)
    arq.write('%d %d %d\n' % (tam, qntNeuroniosEntrada, qntNeuroniosSaida) )
    arq.writelines( padroesValicadao )
    arq.close()
except:
    printError("Impossível gravar os padrões de validação em `%s'" % nomeArqTreino, 5)


try:
    arq = open( nomeArqTeste.split('/')[-1] , 'w' )
    tam = len(padroesTeste)
    arq.write('%d %d %d\n' % (tam, qntNeuroniosEntrada, qntNeuroniosSaida) )
    arq.writelines( padroesTeste )
    arq.close()
except:
    printError("Impossível gravar os padrões de teste em `%s'" % nomeArqTeste, 6)

printMsg("Pronto!")

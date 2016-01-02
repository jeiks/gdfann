#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Jacson RC Silva <jacsonrcsilva@gmail.com>
'''

from algoritmoGenetico.AlgoritmoGenetico import AlgGenetico
from sys import exit

from config import nomeArqValidacao, nomeArqTreino, populacaoInicial, \
                   criterioSatisfacao, maximoGeracoes, logFile

from config_cromossomo import tipoGenes, avaliacaoRNA

try:
    open(nomeArqTreino)
except:
    print "ERRO: Falha ao abrir o arquivo '%s'" % nomeArqTreino
    exit(1)

try:
    open(nomeArqValidacao)
except:
    print "ERRO: Falha ao abrir o arquivo '%s'" % nomeArqValidacao
    exit(1)

# Limpando o arquivo de registros (logs)
open( logFile , "w").close()

# Instância do Algoritmo Genético:
AG = AlgGenetico(tipoGenes, populacaoInicial, avaliacaoRNA, criterioSatisfacao,
                 considMaiorAvaliacao=False, maxGeracoes=maximoGeracoes, verboso=True, distribuido=False)

# Obtendo os resultados:
resultado = AG.evoluir()

# Salvando os resultados:
arqResultado = open("Resultado_Alg-Genetico.txt","w")
for c in resultado:
    arqResultado.write('Cromossomo: ' + str(c))
    arqResultado.write(' - Validacao: '+ str(c.getAvaliacao()) + '\n')
arqResultado.close()


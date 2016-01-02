# -*- coding: utf-8 -*-
'''
@author: Jacson RC Silva <jacsonrcsilva@gmail.com>
'''

import warnings

class Cromossomo:
    '''
    Classe que abriga um Cromossomo de tamanho e
    campos determinados pelo usuário
    '''
    __cromossomo = []
    __qntGenes   = 0 
    __avaliacao  = 0.0

    def __init__(self, qntGenes, cromo=None, avaliacao=0.0):
        ''' Construtor, recebe a quantidade de genes
                        que o cromossomo terá
            @param qntGenes: Quantidade de Genes do Cromossomo 
            @param cromo: Vetor para iniciar o objeto desse cromossomo
            @param avaliacao: Valor de aavliação desse cromossomo
        '''
        self.__avaliacao  = avaliacao
        self.setQntGenes(qntGenes)
        if cromo != None:
            self.__cromossomo = list(cromo)
        else:
            self.__cromossomo = []
    
    def __len__(self):
        return self.__qntGenes
    
    def addGene(self, Gene):
        ''' Adiciona um Gene, se possível, ao final do cromossomo
            @param Gene: Gene para adicionar ao cromossomo
        '''
        if len(self.__cromossomo) > self.__qntGenes:
            warnings.warn("Este gene não pôde ser adicionado,"+
                          "ele já possui o máximo de genes!" %
                          self.__qntGenes, stacklevel=2)
            return False
        else:
            self.__cromossomo.append(Gene)
            return True
            
    def setGene(self, posicao, Gene):
        ''' Define o valor de determinado Gene do Cromossomo 
            pelo valor Gene recebido
            @param posicao: indica a posição a modificar
            @param Gene: Gene para adicionar na posição especificada
        '''
        posicao = int(posicao)
            
        if posicao >= self.__qntGenes:
            #raise Exception("Posição Inválida")
            return False
        else:
            self.__cromossomo[posicao] = Gene
            return True    
    
    def getGene(self, posicao):
        ''' Retorna o Gene de Determinada posição do cromossomo
            @param posicao: Posição desejada do Gene a obter
        '''
        posicao = int(posicao)

        try:
            return self.__cromossomo[posicao]
        except:
            return 0
        
    def getSize(self):
        ''' @return: Retorna o tamanho do cromossomo
        '''
        return len(self.__cromossomo)
    
    def setQntGenes(self, qntGenes):
        ''' Define a quantidade máxima de Genes
            que o cromossomo pode ter
            @param qntGenes: número de cromossomos
        '''
        self.__qntGenes = qntGenes
        if len(self.__cromossomo) > self.__qntGenes:
            warnings.warn("Diminiundo o cromossomo para %d genes" %
                                        self.__qntGenes, stacklevel=2 )
            self.__cromossomo = self.__cromossomo[0:self.__qntGenes]

    def getQntGenes(self):
        ''' @return: retorna o número máximo de Genes
                     que o cromossomo pode ter
        '''
        return self.__qntGenes
    
    def setCromossomo(self, cromo):
        ''' Define todos os genes do cromossomo
            @param cromo: cromossomo
        '''
        if len(cromo) != self.__qntGenes:
            raise Exception("Quantidade de Genes Errada")
        else:
            self.__cromossomo = cromo
            return True
    
    def getCromossomo(self, posicoes=None):
        ''' @return: Retorna o cromossomo inteiro ou uma parte do mesmo
            @param posicoes: Lista de dois elementos, indicando a
                             posição de início e de fim do cromossomo
        '''
        if posicoes == None:
            if len(self.__cromossomo) < self.__qntGenes:
                warnings.warn("O Cromossomo não está completo",
                              stacklevel=2)
                print self.__cromossomo
            return self.__cromossomo
        elif len(posicoes) != 2:
            raise Exception("O arg. 2 deve ser uma lista de dois itens")
        else:
            return self.__cromossomo[ posicoes[0]:posicoes[1] ]
            
    def getPosOf(self, valor):
        ''' @return: retorna a posição do Gene
                     correspondente ao @param valor
            @param valor: valor do Gene a procurar no cromossomo
        '''
        try:
            return self.__cromossomo.index(valor)
        except:
            return -1

    def getQntPosicoesVazias(self):
        ''' @return: Retorna a quantidade de posições não preenchidas
                     do cromossomo
        '''
        return self.__qntGenes - len(self.__cromossomo)

    def setAvaliacao(self, valor):
        ''' Define seu valor de avaliação (aptidão)
            @param valor: valor de avaliação
        '''
        self.__avaliacao = valor
    
    def getAvaliacao(self):
        ''' @return: valor de avaliação 
        '''
        return self.__avaliacao
    
    def clean(self):
        ''' Limpa o cromossomo e sua avaliação
        '''
        self.__avaliacao  = 0.0
        self.__cromossomo = []
    
    def __repr__(self):
        r = ""
        for i in self.__cromossomo:
            r += str(i) + " "
        return r
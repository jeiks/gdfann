# -*- coding: utf-8 -*-
'''
@author: Jacson RC Silva <jacsonrcsilva@gmail.com>
'''

from Populacao import Populacao

class AlgGenetico:
    ''' Algoritmo Genético
        Esta classe visa facilitar a utilização do Algoritmo Genético
        formado pelas classes Cromossomo e População
    '''
    __tipoGenes     = None
    __qntIndividuos = None
    __funcaoAvaliacao    = None
    __criterioSatisfacao = None
    __considMaiorAvaliacao = None
    __maxGeracoes     = None
    __Populacao       = None
    __retCromo        = None
    __verboso         = None
     
    def __init__(self, tipoGenes, qntIndividuos, funcaoAvaliacao,    \
            criterioSatisfacao=0.0, considMaiorAvaliacao=True,      \
            maxGeracoes=10, verboso=False, retCromo=True, distribuido=False):
        ''' Construtor da classe
            @param tipoGenes: Matriz com os tipos de Genes que podem
                            ser utilizados nos indivíduos 
            @param qntIndividuos: Quantidade de indivíduos que uma 
                            população pode ter
            @param funcaoAvaliacao: Função externa que deverá receber o
                            Cromossomo como parâmetro e
                            retornar seu valor de satisfação
            @param criterioSatisfacao: valor de satisfação esperado
                            pelo cromossomo (critério de
                            satisfação)
            @param considMaiorAvaliacao: Informa que os indivíduos com
                            os valores menor devem ser
                            descartados.
                            Para descartar os indivíduos 
                            com o    maior valor, utilize
                            considMaiorAvaliacao=False
            @param maxGeracoes: Informa qual o máximo de gerações, ou
                            seja, o máximo de cruzamentos
                            realizados.
                            O padrão é maxGeracoes=0, onde o
                            critério de término será o
                            "criterioSatisfacao" 
            @param verboso: Imprime mensagens na tela no decorrer do
                            processo
            @param retCromo: Indica se a função de avaliação vai trabalhar com o
                            Cromossomo(True) ou com seu vetor(False)
        '''
        try:
            if type(tipoGenes[0]) != type( list() ):
                raise Exception("ERRO: tipoGenes deve ser uma matriz!")
        except:
            raise Exception("ERRO: tipoGenes deve ser uma matriz!")
        self.__tipoGenes            = tipoGenes
        self.__qntIndividuos        = qntIndividuos
        self.__funcaoAvaliacao      = funcaoAvaliacao
        self.__criterioSatisfacao   = criterioSatisfacao
        self.__considMaiorAvaliacao = considMaiorAvaliacao
        self.__maxGeracoes          = maxGeracoes
        self.__retCromo             = retCromo
        self.__verboso              = verboso
        self.__Populacao            = None        
        self.__distribuido          = distribuido
    
    def ordenaPorAvaliacao(self, cromo):
        ''' Método que devolve a avaliação do cromossomo
            @param: Cromossomo
            @return: Avaliação do cromossomo
        '''
        return cromo.getAvaliacao()
    
    def verCriterioTerminacao(self):
        ''' Verifica se algum dos cromossomos atingiu o critério de
            término
            @return:
                True -> a população alcançou a critério de término
                False -> a população não alcançou a critério de término
        '''
        retorno = []
        for cromo in self.__Populacao.getIndividuos():
            if self.__considMaiorAvaliacao:
                if cromo.getAvaliacao() >= self.__criterioSatisfacao:
                    retorno.append( cromo )
            else:
                if cromo.getAvaliacao() <= self.__criterioSatisfacao:
                    retorno.append( cromo )
                    
        retorno.sort(key=self.ordenaPorAvaliacao,
                     reverse=self.__considMaiorAvaliacao)
        if len( retorno ) == 0:
            return False, retorno
        else:
            return True, retorno
                
    
    def evoluir(self):
        ''' Método responsável por controlar toda a execução do
            algoritmo genético, incluindo os cruzamentos e a mutação
            @return: a última população de cromossomos
        '''
        retorno = []
        
        self.__Populacao = Populacao( self.__tipoGenes, distribuido=self.__distribuido, maiorValor=self.__considMaiorAvaliacao )
        self.__Populacao.gerarPopulacao( self.__qntIndividuos )
        self.__Populacao.avaliarPopulacao( self.__funcaoAvaliacao )
        if self.__criterioSatisfacao != 0.0:
            resp, cromos = self.verCriterioTerminacao()
                    
        Ger = 1         
        if self.__maxGeracoes == 0:
            while not resp:
                self.__Populacao.geraNovaPopulacao(
                             self.__funcaoAvaliacao,
                                   self.__considMaiorAvaliacao)
                resp, cromos = self.verCriterioTerminacao()
            
            if self.__verboso:
                print "Indivíduos que alcançaram o critério de Satisfação:"

            for i in cromos:
                retorno.append(i)
                if self.__verboso:
                    print i.getCromossomo(), i.getAvaliacao()
        elif self.__criterioSatisfacao != 0.0:
            while not resp and Ger <= self.__maxGeracoes:
                if self.__verboso: print "Geração:", Ger
                self.__Populacao.geraNovaPopulacao(
                                           self.__funcaoAvaliacao,
                                           self.__considMaiorAvaliacao)
                
                resp, cromos = self.verCriterioTerminacao()
                Ger+=1
            
            if resp:
                if self.__verboso:
                    print "Indivíduos que alcançaram o critério de Satisfação:"
                for i in cromos:
                    retorno.append(i)
                    if self.__verboso:
                        print i.getCromossomo(), i.getAvaliacao()
            else:
                if self.__verboso:
                    print "Indivíduos não alcançaram o critério de Satisfação!"
                if self.__verboso: print "A última população foi:"
                for i in self.__Populacao.getIndividuos():
                    retorno.append(i)
                    if self.__verboso:
                        print i.getCromossomo(), i.getAvaliacao()
        else:
            for Ger in range(self.__maxGeracoes):
                if self.__verboso: print "Geração:", Ger
                self.__Populacao.geraNovaPopulacao(
                                   self.__funcaoAvaliacao,
                                   self.__considMaiorAvaliacao,
                                   self.__retCromo)
            
            if self.__verboso: print "A última população foi:"
            for i in self.__Populacao.getIndividuos():
                retorno.append(i)
                if self.__verboso:
                    print i.getCromossomo(), i.getAvaliacao()
        return retorno

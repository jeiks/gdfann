# -*- coding: utf-8 -*-
'''
@author: Jacson RC Silva <jacsonrcsilva@gmail.com>
'''

from Cromossomo import Cromossomo
import warnings
from threading import Thread
from time import sleep
import jsonrpclib
from config import nodes

printMsgWait = True

class AvaliacaoCromossomo(Thread):
        def __init__(self, cromo, funcao):
            Thread.__init__(self)
            self._cromo  = cromo
            self._funcao = funcao
            self._resp   = 999.9
            
        def run(self):
            self._resp = self._funcao( self._cromo )
        
        def getResp(self):
            return self._resp


class AvaliacaoPopulacao(Thread):
    
    def __init__(self, populacao, client):
        Thread.__init__(self)
        self._populacao = populacao
        self._client    = client
    
    def run(self):
        server = jsonrpclib.Server('http://%s:5000' % self._client)
        a = []
        for i in self._populacao:
            a.append(i.getCromossomo())
        print 'Enviando', a, 'para', self._client
        self._answers = server.run(a)
        
    def obterAvaliacoes(self):
        return self._answers

class Populacao:
    ''' Classe responsável pelo controle da população de
        cromossomos(indivíduos)
    '''
    __individuos          = None
    __velhaPopulacao      = None
    __historicoIndividuos = None
    __matrizPossib        = None
    # individuos já avaliados?
    __indAvaliados        = None
    # velha população já avaliada?
    __velPopAvaliada      = None
    __verboso             = None
    # paralelização da avaliação da população
    __paralelo            = None
    __threads_pool        = None
    __distribuido         = None
    
    def __init__(self, matrizPossib, verboso=True, distribuido=False, maiorValor=True):
        ''' Cronstutor padrão
            @param matrizPossib: matriz com as possibilidades de genes
                       existentes
            ex: [ [0,1] , ['a','b'] , [func1,func2] ]
        '''
        self.__individuos          = []
        self.__velhaPopulacao      = []
        self.__historicoIndividuos = []
        self.__matrizPossib        = matrizPossib
        self.__indAvaliados        = False
        self.__velPopAvaliada      = False
        self.__verboso             = verboso
        self.__paralelo            = True
        self.__threads_pool        = []
        self.__distribuido         = distribuido
        self.__maiorValor          = maiorValor
    
    def addIndividuo(self, cromo):
        ''' Adiciona um indivíduo a população
            @param cromo: Cromossomo (indivíduo) a adicionar
        '''
        self.__individuos.append(cromo)
    
    def getIndividuo(self, posicao):
        ''' Método para obter um indivíduo específico da população
            @param posicao: posição do indivíduo 
            @return: retorna o indivíduo (cromossomo)
        '''
        return self.__individuos[posicao]
    
    def setIndividuo(self, posicao, cromo):
        ''' Troca o indivíduo da população pelo indivíduo recebido
            @param posicao: posição do indivíduo
            @param cromo: novo cromossomo (indivíduo)
        '''
        self.__individuos[ int(posicao) ] = cromo
    
    def getIndividuos(self):
        ''' Método para obter os indivíduos da população
            @return: todos os indivíduos (cromossomos)
        '''
        return self.__individuos
    
    def getAllFitness(self):
        ''' Método para obter o fitness de todos os indivíduos
            @return: fitness de todos individuos
        '''
        ret = []
        for i in self.getIndividuos():
            ret.append(i.getAvaliacao())

        return list(ret)
    
    def gerarPopulacao(self, qntIndividuos):
        ''' Método para gerar uma população aleatória
            @param qntIndividuos: quantidade de indivíduos da população
        '''
        from random import choice
        # o número de indivíduos deve ser par
        # devido ao método de cruzamento
        qntIndividuos += qntIndividuos%2
        while qntIndividuos > 0:
            individuo = Cromossomo( len(self.__matrizPossib))
            
            for gene in self.__matrizPossib:
                individuo.addGene( choice(gene) )
                
            self.addIndividuo(individuo)
            del(individuo)
            
            qntIndividuos-=1
        
        self.__indAvaliados = False
        try: del(self.__roleta)
        except: pass

    def dividirPopulacao(self, populacao=None, qntsPartes=1):
        if populacao is None: populacao = self.__individuos
        tam = len(populacao)
        return [ populacao[i*tam // qntsPartes: (i+1)*tam // qntsPartes] for i in range(qntsPartes) ]

    def avaliarPopulacao(self, funcao, avaliarInd=True, retCromo=True):
        ''' Percorre os indivíduos, executando a função de ativação
            fornecida para cada indivíduo.
            @param funcao: funcao de avaliacao de cada indivíduo
            @param avaliarInd:
                         True  -> Avaliar os Indivíduos dessa população
                         False -> Avaliar a velha população
            @param retCromo:
                         True  -> utiliza o cromossomo na função
                         False -> utiliza o vetor de genes na função
        '''
        if avaliarInd:
            pop = self.__individuos
            self.__indAvaliados = True
        else:
            pop = self.__velhaPopulacao
            self.__velPopAvaliada = True
        
        if self.__distribuido:
            vetPop = self.dividirPopulacao(pop, len(nodes)+1)
            pop    = vetPop[0]
            nodeExterno = []
            for i in range(1, len(vetPop)):
                print 'Preparando node Externo', i-1
                nodeExterno.append( AvaliacaoPopulacao(vetPop[i], nodes[i-1]) )
                nodeExterno[-1].start()
        
        #PARALELIZANDIOOO....
        if self.__verboso: print 'Avaliando a população em paralelo.'
        threads = []
        grupos_threads = 7
        # sincronização
        threads_executando = [False]*len(pop)
        threads_terminadas = [False]*len(pop)
        
        for c in pop:
            if retCromo:
                threads.append( AvaliacaoCromossomo(c, funcao) )
            else:
                threads.append( AvaliacaoCromossomo(c.getCromossomo(), funcao) )
                
        global printMsgWait
        while threads_terminadas.count(False) > 0:
            count = 0
            while threads_executando.count(True) < grupos_threads and count < len(pop):
                if not threads_terminadas[count] and not threads_executando[count]:
                    if self.__verboso: print 'Avaliando o cromossomo %d.' % count
                    threads[count].start()
                    threads_executando[count] = True
                count = count+1

            if self.__verboso and printMsgWait: 
                verb_qnt = threads_terminadas.count(False)
                print 'Esperando %d cromossomo%s terminar%s sua execução...' % (verb_qnt, ('s' if verb_qnt > 1 else ''), ('em' if verb_qnt > 1 else ''))
                printMsgWait = False

            for i in range(0, len(pop)):
                if threads_executando[i]:
                    if not threads[i].isAlive():
                        if self.__verboso:
                            print 'A avaliação do cromossomo %d acabou.' % i
                            printMsgWait = True
                        threads_terminadas[i] = True
                        threads_executando[i] = False
            sleep(2)
            
        for n in range(len(pop)):
            if self.__verboso: print 'Cromossomo',n,'com avaliacao',threads[n].getResp()
            pop[n].setAvaliacao( threads[n].getResp() )
        
        if self.__distribuido:
            if self.__verboso: print 'Esperando node(s) externo(s) avaliar(em) os demais cromossomos...'
            for i in nodeExterno: i.join()
            
            chrN = len(pop)
            for i in range(len(nodes)):
                avals = nodeExterno[i].obterAvaliacoes()
                for n in range(len(vetPop[i+1])):
                    if self.__verboso: print i,'Cromossomo',chrN,'com avaliacao',avals[n]
                    vetPop[i+1][n].setAvaliacao( avals[n] )
                    chrN += 1

        if self.__verboso: print 'População avaliada. Continuando...'
        
        """
        for i in pop:
            if retCromo:
                i.setAvaliacao( funcao(i) )
            else:
                i.setAvaliacao( funcao(i.getCromossomo()) )
        """
            
    def geraNovaPopulacao(self, funcao, baixos=True, retCromo=True):
        ''' Remove os cromossomos piores
            @param baixos: informa se os piores valores são os mais
                           baixos, caso False, ele considerará piores
                           os mais altos
            @param funcao: funcao de avaliacao de cada indivíduo
            @param retCromo:
                        True  -> utiliza o cromossomo na função
                        False -> utiliza o vetor de genes na função
        '''
        def ordenacao(cromo):
            return cromo.getAvaliacao()
        
        if self.__velhaPopulacao == []:
            if self.__verboso: print 'Fazendo Cruzamento...'
            try: del(self.__roleta)
            except: pass
            self.fazerCruzamento()
            if self.__verboso: print 'Fazendo Mutação...'
            self.fazerMutacao()
        
        if not self.__indAvaliados:
            if self.__verboso: print 'Avaliando indivíduos dessa população...'
            self.avaliarPopulacao(funcao, avaliarInd=True, retCromo=retCromo)

        if not self.__velPopAvaliada:
            if self.__verboso: print 'Avaliando velha população...'
            self.avaliarPopulacao(funcao, avaliarInd=None,
                                  retCromo=retCromo)
        
        qntInd   = self.getQntIndividuos()
        qntElite = int(qntInd*0.1)
        qntRest  = qntInd - qntElite
         
        # para obter a elite:
        novosIndividuos = list(self.__individuos+self.__velhaPopulacao)
        # ordenando elite
        novosIndividuos.sort(key=ordenacao, reverse=baixos)
        # deixando 10% dos melhores cromossomos
        elite = novosIndividuos[:qntElite]
        
        # removendo a elite da lista para pegar os demais
        novosIndividuos = list(self.__individuos+self.__velhaPopulacao)
        for i in elite:
            novosIndividuos.remove(i)
        novosIndividuos = novosIndividuos[:qntRest]
        # os individuos são definidos como 
        self.__individuos = list(elite + novosIndividuos)         
        self.__velhaPopulacao = []
        self.__velPopAvaliada = False
        del(novosIndividuos)
        del(elite)

    def getSize(self):
        ''' Idem getQntIndividuos
        '''
        return self.getQntIndividuos()
        
    def getQntIndividuos(self):
        ''' @return: Retorna a quantidade de Indivíduos
        '''
        return len(self.__individuos)
    
    def __cruzar(self, ind1, ind2):
        ''' Método que faz o cruzamento entre dois indivíduos
            (Cromossomos)
            @param ind1: indivíduo a sofrer mutação
            @param ind2: indivíduo a sofrer mutação
        '''
        from random import randint
        cruzamentos = randint(1, len(self.__matrizPossib)/2)
        cut = randint(1,len(self.__matrizPossib)-2)
        retorno = [ ind1.getCromossomo()[:cut]+
                    ind2.getCromossomo()[cut:]
                    ,
                    ind2.getCromossomo()[:cut]+
                    ind1.getCromossomo()[cut:]
                  ]
        cruzamentos-=1
        while cruzamentos > 0:
            cut = randint(1,len(self.__matrizPossib)-2)
            retorno = [ retorno[0][:cut]+retorno[1][cut:] ,
                        retorno[1][:cut]+retorno[0][cut:]  ]
            cruzamentos-=1
        return [ Cromossomo( len(retorno[0] ), retorno[0] ),
                 Cromossomo( len(retorno[1] ), retorno[1] )  ]
    
    def verificarDuplo(self, cromo):
        ''' Verifica se o individuo (cromossomo) já existe na população
            @param cromo: cromossomo a avaliar
            @param usarHistorico: guarda o histórico de todos os
                                  indivíduos
            @return: True  -> indivíduo já existe na população
                     False -> indivíduo não existe a população
        '''
        for i in self.__velhaPopulacao:
            if i.getCromossomo() == cromo.getCromossomo():
                return True
        return False
       
    def roleta(self):
        from random import random
        
        fitness = self.getAllFitness()
        auxMax = max(fitness)
        auxMin = min(fitness)
        if not self.__maiorValor:
            fitness = map(lambda x: (auxMax+auxMin/2) - x, fitness)

        try:
            roleta = self.__roleta
        except AttributeError:
            self.__roleta = []
            soma = 0.0
            for i in fitness:
                self.__roleta.append(i+soma)
                soma += i
            roleta = self.__roleta
        
        c1, c2 = (0,0)
        roleta = [0] + roleta
        while c1 == c2:
            #sorteio:
            val1 = random()*(max(roleta))
            val2 = random()*(max(roleta))
            count = len(roleta)-1
            while count >= 0 and (val1 <> -1 or val2 <> -1):
                if val1 > roleta[count]:
                    c1 = count
                    val1 = -1
                if val2 > roleta[count]:
                    c2 = count
                    val2 = -1
        
                count -= 1
        
        return c1, c2
    
    def fazerCruzamento(self):
        ''' Realiza o cruzamento entre os indivíduos da População
        '''
        if len(self.__individuos) < 1:
            warnings.warn("Primeiro gere uma população com " \
                          "mais de 1 elemento", stacklevel=2)
            from sys import exit
            exit(1)
        else:
            from random import randint
            self.__velhaPopulacao = list(self.getIndividuos())
            self.__velPopAvaliada = self.__indAvaliados
            self.__historicoIndividuos += self.__velhaPopulacao

            novaPopulacao = []
            # criando uma população com a mesma quantidade de individuos
            for i in range(self.getQntIndividuos()/2):
                #sorteia dois individuos usando a roleta:
                ind1, ind2 = self.roleta()

                #faz o cruzamento até encontrar um individuo que
                # ainda nao pertence a populacao (loop máximo de 30 vezes)
                tentativas    = 30
                ret1_OK       = False
                ret2_OK       = False
                while (not ret1_OK or not ret2_OK) and tentativas > 0:
                    ret1, ret2 = self.__cruzar(self.__velhaPopulacao[ind1], self.__velhaPopulacao[ind2])
                    
                    if not ret1_OK:
                        if not self.verificarDuplo(ret1):
                            novaPopulacao.append(ret1)
                            ret1_OK = True
                    
                    if not ret2_OK:
                        if not self.verificarDuplo(ret2):
                            novaPopulacao.append(ret2)
                            ret2_OK = True

                    tentativas -= 1
            
            if len(self.__individuos) <> len(novaPopulacao):
                print 'CUIDADO: Não foi possível gerar filhos diferentes dos que já foram gerados no passado'
                print '         Com isso, a população atual possui menos indivíduos'
                print '         Para corrigir, serao adicionados individuos aleatorios da populacao antiga'
                # nao permite que a populacao nova tenha menos individuos que a atual
                while len(self.__individuos) <> len(novaPopulacao):
                    novaPopulacao.append( self.__individuos[randint(0,len(self.__individuos)-1)] ) 
            self.__individuos = []
            for i in novaPopulacao: self.addIndividuo(i)
            self.__indAvaliados = False

    def fazerMutacao(self):
        from random import randint
        # a crazy comparation... but we have users... :P
        # testa se tem uma posição de genes com mais de uma opção
        aux = map(lambda x: len(x) == 1, self.__matrizPossib)
        try:    aux.index(False)
        except: return
        
        # para todos os indivíduos:
        for i in range(self.getQntIndividuos()):
            # verifica se deve mutar:
            if randint(1,10) == 7:
                # qual gene mutar:
                pos_gene = randint(0, len(self.__matrizPossib)-1 )
                while len(self.__matrizPossib[pos_gene]) <= 1:
                    pos_gene = randint(0, len(self.__matrizPossib)-1 )
                gene_atual = self.__individuos[i].getGene(pos_gene)
                gene_novo  = self.__matrizPossib[pos_gene][ randint(0,len(self.__matrizPossib[pos_gene])-1) ]
                while gene_atual == gene_novo:
                    gene_novo  = self.__matrizPossib[pos_gene][ randint(0, len(self.__matrizPossib[pos_gene])-1) ]
                        
                self.__individuos[i].setGene(pos_gene, gene_novo)
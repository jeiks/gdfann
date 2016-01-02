#!/usr/bin/env python
#-*- coding: utf-8 -*-

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from algoritmoGenetico.Populacao import Populacao
from algoritmoGenetico.Cromossomo import Cromossomo
from config_cromossomo import avaliacaoRNA    

class GDFANN_Node:
    def __init__(self, domain='0.0.0.0', port=5000):
        self._server = SimpleJSONRPCServer( (domain, port) )
        functions = {
                     'run' : self.run
                    }

        for name in functions.keys():
            self._server.register_function(functions[name], name)
        self._pop = None

    def run(self, population):
        if type(population) <> list:
            return 'Population must be a list'
        
        if self._pop is not None: del(self._pop)
        
        self._pop = Populacao(None, verboso=True)
        
        for i in population:
            print i
            self._pop.addIndividuo(Cromossomo(9,i))
        
        print 'Evaluating population...'
        self._pop.avaliarPopulacao(avaliacaoRNA)
        print 'Sending answers...'
        answersMSE = []
        for i in self._pop.getIndividuos():
            answersMSE.append(i.getAvaliacao())
        print answersMSE
        return answersMSE

    def serve(self):
        try:
            print 'Server running. Press CTRL+C to stop...'
            self._server.serve_forever()
        except KeyboardInterrupt:
            print 'Exiting'

if __name__ == "__main__":
    server = GDFANN_Node()
    server.serve()

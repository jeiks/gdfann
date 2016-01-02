CC     := /usr/bin/gcc
CFLAGS := -lm -lfann

build: buildPatterns Avaliador_Fann
	@echo -e '\n\033[31;2mInicie a execução do Algoritmo Genético executando: \033[32;2m./RNAGenetico.py\033[0m\n'

buildHeader:
	@chmod +x build_header.py
	@./build_header.py

Avaliador_Fann: buildHeader
	@#usado na execucao do Algoritmo Genetico
	$(CC) -o Avaliador_Fann Avaliador_Fann.c $(CFLAGS)

teste_RNA:
	@#usado apos executar o algoritmo genetico
	$(CC) -o teste_RNA      teste_RNA.c      $(CFLAGS)

clean:
	rm -f teste_RNA Avaliador_Fann Avaliador_Fann.h .tempResults
	find -name '*.pyc' -delete

buildPatterns:
	cd entradas && make

cleanPatterns:
	cd entradas && make clean

distclean: clean cleanPatterns
	rm -rf Execucao_Alg_Gen.log Resultado_Alg-Genetico.txt Redes_Geradas results_plots results_tests

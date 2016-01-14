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

clean:
	rm -f Avaliador_Fann Avaliador_Fann.h .tempResults
	find -name '*.pyc' -delete

teste_RNA:
	cd utils && make teste_RNA

teste_RNA_with_effort:
	cd utils && make teste_RNA_with_effort

clean_teste_RNA:
	cd utils && make clean

buildPatterns:
	cd entradas && make

cleanPatterns:
	cd entradas && make clean

distclean: clean cleanPatterns clean_teste_RNA
	rm -rf Execucao_Alg_Gen.log Resultado_Alg-Genetico.txt Redes_Geradas results_plots results_tests
	cd utils && make clean

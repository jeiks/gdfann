

criarPadroesFANN: gerarTodosDados gerarEntrada
	./gerarEntrada todos_dados.txt 120 > todos_dados.fann

gerarTodosDados:
	bash -c 'cat results_pid/results_pid-velocity-20140320-* > todos_dados.txt'

gerarEntrada: gerarEntrada.c

clean:
	rm -f gerarEntrada todos_dados.fann todos_dados.txt

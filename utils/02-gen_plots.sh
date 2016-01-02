#!/bin/bash

[ ! -d ../RNAs ] && {
    echo "ERRO: Não foi possível encontrar a pasta '../RNAs'"
    echo 'Execute o script 01-copiar_redes.sh ou verifique se está executando este script pasta principal.'
    exit 1
}


[ ! -f teste_RNA ] && make teste_RNA

DIR_OUTPUTS='results_tests'
DIR_PLOTS='results_plots'
ARQ_TESTES=$(python -c 'from config import nomeArqTeste;print nomeArqTeste') 

mkdir -p $DIR_OUTPUTS $DIR_PLOTS

for i in ../RNAs/*;do
    N=`basename ${i}`
    N=${N%-*}
    ./teste_RNA $i $ARQ_TESTES > $DIR_OUTPUTS/teste_RNA-$N.txt
    ./utils/03-org_graph.py <(grep ^Resultado $DIR_OUTPUTS/teste_RNA-${N}.txt) $DIR_OUTPUTS/teste_RNA-${N}_quarto.txt
    MSE=$(awk '{if ($5 == "Mean") print $NF}' $DIR_OUTPUTS/teste_RNA-${N}.txt)
    ARQ="$DIR_OUTPUTS/teste_RNA-${N}_quarto.txt"
    echo "set term pngcairo font 'Times New Roman,10';
          set output '${DIR_PLOTS}/figura_${N}.png';
          set title 'ANN $N (MSE: $MSE)';
          plot '$ARQ' using 2 title 'Estimated' with lines, '$ARQ' using 4 title 'Desired' with lines, '$ARQ' using 6 title 'Error' with lines" | gnuplot

done

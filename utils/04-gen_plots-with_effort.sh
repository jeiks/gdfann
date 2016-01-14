#!/bin/bash

[ ! -d ../RNAs ] && {
    echo "ERRO: Não foi possível encontrar a pasta '../RNAs'"
    echo 'Execute o script 01-copiar_redes.sh ou verifique se está executando este script pasta principal.'
    exit 1
}


[ ! -f teste_RNA_with_effort ] && make teste_RNA_with_effort

DIR_OUTPUTS='results_tests'
DIR_PLOTS='results_plots'
ARQ_TESTES=$(python -c 'from config import nomeArqTeste;print nomeArqTeste') 

mkdir -p $DIR_OUTPUTS $DIR_PLOTS

for i in ../RNAs/*;do
    N=`basename ${i}`
    N=${N%%-*}
    ./teste_RNA_with_effort $i $ARQ_TESTES > $DIR_OUTPUTS/teste_RNA-$N.txt
    for JUMP in 1 4 8;do
        ./utils/03-org_graph.py $JUMP <(grep ^Resultado $DIR_OUTPUTS/teste_RNA-${N}.txt) $DIR_OUTPUTS/teste_RNA-${N}_${JUMP}.txt
        MSE=$(awk '{if ($5 == "Mean") print $NF}' $DIR_OUTPUTS/teste_RNA-${N}.txt)
        ARQ="$DIR_OUTPUTS/teste_RNA-${N}_${JUMP}.txt"
        echo "set term pngcairo font 'Times New Roman,10' size 1024,768;
              set output '${DIR_PLOTS}/figura_${N}_${JUMP}.png';
              set title 'ANN (MSE: $MSE) $N 1/${JUMP}';
              plot '$ARQ' using 2 title 'Estimated' with lines, \
                   '$ARQ' using 4 title 'Desired' with lines, \
                   '$ARQ' using 6 title 'Error' with lines, \
                   '$ARQ' using 8 title 'Throttle/10' with lines lc rgb '#007cad', \
                   '$ARQ' using 10 title 'Brake/100' with lines lc rgb '#0fdd11'" | gnuplot
    done

done

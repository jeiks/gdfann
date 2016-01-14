#!/bin/bash

ARQ_RESULTADOS='Resultado_Alg-Genetico.txt'
ARQ_TEMP='.tempResults'
ARQ_VALIDACAO='entradas/validacao.train'
TESTE_RNA='utils/teste_RNA'

[ ! -f $ARQ_RESULTADOS ] && {
    echo "ERRO: Não foi possível abrir o arquivo $ARQ_RESULTADOS"
    echo 'Execute o algoritmo genético ou verifique se está executando este script pasta principal.'
    exit 1
}

mkdir -p ../RNAs

awk '{for (i=2;i<10;i++) {printf "%s_",$i}; printf $10".net "$NF"\n";}' $ARQ_RESULTADOS > $ARQ_TEMP

[ ! -f $TESTE_RNA ] && make teste_RNA

FANN_VERSION_2=$( (ldd $TESTE_RNA | grep -q /usr/lib/x86_64-linux-gnu/libfann.so.2) && echo 0 || echo 1)

NUM=1
while read RNA MSE;do
    MSE=$(awk '{printf "%.6f",$1}' <<< $MSE)
    RNA_aux="${RNA%.net}*.net"
    for R in $(find .. -name "$RNA_aux");do
        if [ "$FANN_VERSION_2" = 1 ];then
        	if ! grep -q cascade_min_out_epochs $R;then
        		sed -i -e '22i\' -e 'cascade_min_out_epochs=10' $R
        		sed -i -e '24i\' -e 'cascade_min_cand_epochs=10' $R
        	fi
        else
            grep -v cascade_min_ $R > /tmp/.rna_temp
            mv -f /tmp/.rna_temp $R
        fi
        M=$(./$TESTE_RNA $R $ARQ_VALIDACAO | grep Mean\ Sq| awk '{printf "%.6f",$NF}')
        if [ "$M" = "$MSE" ];then
            cp -v $R ../RNAs/$(printf "%03d" $NUM)-${R##*/}
            break
        fi
    done
    let NUM++
done < $ARQ_TEMP




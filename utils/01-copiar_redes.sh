#!/bin/bash

ARQ_RESULTADOS='Resultado_Alg-Genetico.txt'
ARQ_TEMP='.tempResults'
ARQ_VALIDACAO='entradas/validacao.train'

[ ! -f $ARQ_RESULTADOS ] && {
    echo "ERRO: Não foi possível abrir o arquivo $ARQ_RESULTADOS"
    echo 'Execute o algoritmo genético ou verifique se está executando este script pasta principal.'
    exit 1
}

mkdir -p ../RNAs

awk '{for (i=2;i<10;i++) {printf "%s_",$i}; printf $10".net "$NF"\n";}' $ARQ_RESULTADOS > $ARQ_TEMP

[ ! -f teste_RNA ] && make teste_RNA

FANN_VERSION_2=$( (ldd teste_RNA | grep -q /usr/lib/x86_64-linux-gnu/libfann.so.2) && echo 0 || echo 1)

NUM=1
while read RNA MSE;do
    ACHOU=0
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
        M=$(./teste_RNA $R $ARQ_VALIDACAO | grep Mean\ Sq| awk '{print $NF}')
        # fix exponential
        case $MSE in *'e'*) MSE=$(awk '{printf "%f",$1}' <<< $MSE);; esac
        if [ "$M" = "$MSE" ];then
            cp -v $R ../RNAs/$(printf "%03d" $NUM)-${R##*/}
            ACHOU=1
            break
        fi
    done
    [ $ACHOU -eq 0 ] && {
        echo "Não foi possível achar a RNA: $RNA"
        echo "Copiando $R no lugar, pois tem a mesma configuração."
        cp -v $R ../RNAs/$(printf "%03d" $NUM)-${R##*/}
    }
    let NUM++
done < $ARQ_TEMP




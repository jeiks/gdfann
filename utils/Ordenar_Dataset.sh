#!/bin/bash

[ $# -ne 3 ] && {
    echo "Use: $0 arqDoDataset arqComTodosPadroes arqSaida"
    exit 1
}

ARQ_DATASET=$1
ARQ_TODOS_PADROES=$2
ARQ_SAIDA=$3

echo -n '
 O que deseja fazer:
[1] usar todos padrões (incluindo repetidos)
[2] usar somente o primeiro que casar
:: '
read resp
case $resp in
    1*)
        echo 'ok, usando todos os padrões'
        MATCH=''
        ;;
    *)
        echo 'ok, usando somente o primeiro padrão que casar com o original'
        MATCH='-m 1'
        ;;
esac

echo "Removendo a primeira linha de '$ARQ_DATASET'..."
tail -n +2 $ARQ_DATASET > $ARQ_DATASET.temp

echo "Adicionando coluna de tempo em '$ARQ_TODOS_PADROES'..."
nl $ARQ_TODOS_PADROES   > $ARQ_TODOS_PADROES.temp

echo -n 'Buscando padrões...'
while read LIN;do
    echo -n '.' >&2
    let NUM++
    grep $MATCH "$LIN" $ARQ_TODOS_PADROES.temp
done < $ARQ_DATASET.temp > .temp
echo ok

echo "Ordenando os padrões..."
sort -n -k 1 .temp > $ARQ_DATASET.temp

echo "Removendo a coluna de tempo..."
cut -d "$(echo -e '\t')" -f2 < $ARQ_DATASET.temp > .temp

echo "Escrevendo arquivo de saida: '$ARQ_SAIDA'..."
INFO_1=$(wc -l .temp | cut -d ' ' -f1)
INFO_2=$(head -n 1 $ARQ_DATASET | cut -d' ' -f2-)
echo $INFO_1 $INFO_2 > $ARQ_SAIDA
cat .temp           >> $ARQ_SAIDA

rm .temp $ARQ_DATASET.temp $ARQ_TODOS_PADROES.temp

echo Pronto

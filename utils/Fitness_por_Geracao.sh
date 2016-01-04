#!/bin/bash

[ ! -f LOG ] && {
    echo 'O arquivo `LOG'\'' é necessário para executar esse script.'
    exit 1
}

FITNESS_GERACAO=''
LAST=9999.9
NUM=1
grep 'Cromossomo\|Continuando' LOG | while read LINHA;do
    case "$LINHA" in
        *Cromossomo*)
            FITNESS_GERACAO="$FITNESS_GERACAO\n${LINHA##* }"
            ;;
        *Continuando*)
            echo "Geracao $NUM:"
            F=$(sort -n < <(echo -e "${FITNESS_GERACAO//./,}" | grep -v '^$') | head -n1 | tr , .)
            MENOR=$(python -c "print 1 if ($F < $LAST) else 0")
            if [ $MENOR = "1" ];then
                LAST=$F
                echo $F
            else
                echo $LAST
            fi
            let NUM++
            FITNESS_GERACAO=''
            ;;
        *)
            echo nao conheco essa linha.
    esac
done

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import argv, exit

if len(argv) <> 4:
    print "Use: %s [1|4|8] arqEntrada arqSaida" % argv[0]
    exit(1)

jump       = int(argv[1])
arqEntrada = argv[2]
arqSaida   = argv[3]
orig = open(arqEntrada).readlines()[2:-2]
open(arqSaida,'w').writelines(orig[0::jump])

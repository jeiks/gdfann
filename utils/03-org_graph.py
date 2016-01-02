#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import argv, exit

if len(argv) <> 3:
    print "Use: %s arqEntrada arqSaida" % argv[0]
    exit(1)

orig = open(argv[1]).readlines()[2:-2]
open(argv[2],'w').writelines(orig[0::4])

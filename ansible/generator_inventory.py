#!/usr/bin/python3

import json
import sys, getopt

# Arquivo de inventario
inventory_file = "inventory.json"

# ip base do cluster
ip_base = "192.168.247.{m}"

# ip inicial das maquinas do cluster
ip_ini = 125

inventory = {'all' : { 'hosts' : {}}}

size = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:",["size="])
except getopt.GetoptError:
      print ('./inventory_generator -s <n>')
      sys.exit(2)

for opt, arg in opts:
    if opt == "-h":
        print('./inventory_generator -s <n>')
        sys.exit()
    elif opt in ("-s","--size"):
        size = int(arg)

        if (size <= 0 ):
            print("Tamanho inválido do cluster!\n")
            sys.exit(2)


try:
    f = open(inventory_file, 'w')
    
    print("Gerando inventario de hosts com {n} hosts! \n".format(n=size))

    # Guarda hosts no inventario
    for i in range(size):
        ip = ip_base.format(m=(ip_ini+i))

        inventory['all']['hosts'][ip] = None

    f.write(json.dumps(inventory))
    f.close()
except:
    print("Erro ao criar arquivo de inventario")

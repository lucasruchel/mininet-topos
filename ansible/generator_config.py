#!/usr/bin/python3

import json
import sys, getopt

# Arquivo de inventario
config_file = "conf.json"

# ip base do cluster
ip_base = "192.168.247.{m}"

# ip inicial das maquinas do cluster
ip_ini = 125

config = {"cluster_ips": []}

size = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"hs:",["size="])
except getopt.GetoptError:
      print ('./generator_config -s <n>')
      sys.exit(2)

for opt, arg in opts:
    if opt == "-h":
        print('./generator_config -s <n>')
        sys.exit()
    elif opt in ("-s","--size"):
        size = int(arg)

        if (size <= 0 ):
            print("Tamanho inválido do cluster!\n")
            sys.exit(2)


try:
    f = open(config_file, 'w')
    
    print("Gerando config de hosts com {n} hosts! \n".format(n=size))

    # Guarda hosts no inventario
    for i in range(size):
        ip = ip_base.format(m=(ip_ini+i))

        config['cluster_ips'].append(ip)

    f.write(json.dumps(config))
    f.close()
except:
    print("Erro ao criar arquivo de config")

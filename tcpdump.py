from os import mkdir, path, system, chdir

def capture(name, interface, timeout=60):
    log_dir = 'capturas/'

    nro_f = 1
    log_file = name + (".%s.pcap" % nro_f)

    while path.exists(log_dir + log_file):
        nro_f += 1
        log_file = name + (".%s.pcap" % nro_f)
    
    if not path.exists(log_dir):
        mkdir(log_dir)
    system("timeout %d sudo tcpdump  -w %s -i %s &" % (timeout,log_dir+log_file,interface))

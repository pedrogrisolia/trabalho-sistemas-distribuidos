import xmlrpc.client
import sys
import time

proxy = xmlrpc.client.ServerProxy('http://localhost:9000', allow_none=True)

def sucuri(nprocs):
	print("Iniciando job de processamento de imagens com %d workers via Sucuri." %nprocs)
	proxy.sucuri(nprocs)
	

t0 = time.time()
sucuri(int(sys.argv[1]))
t1 = time.time()
print("Job concluido em %.3f segundos." %(t1-t0))

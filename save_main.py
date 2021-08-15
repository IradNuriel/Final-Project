import subprocess
import sys
import os

l = os.listdir("weights")
output = subprocess.check_output([sys.executable, './training_main.py'])
ls = os.listdir("weights")
set_difference = list(set(ls) - set(l))[0]

with open('weights\\' + set_difference + '\\log.txt', 'wb') as outfile:
    outfile.write(output)

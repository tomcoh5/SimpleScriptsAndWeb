# simple python script for running on linux server 
import subprocess
from random import randint
for i in range(70):
    value = randint(0, 300)
    value2 = randint(0,10000)
    bashcommand = "fallocate -l " + str(value) + "mb file" + str(value2) + ".txt"
    process = subprocess.Popen(bashcommand.split(), stdout=subprocess.PIPE)
    

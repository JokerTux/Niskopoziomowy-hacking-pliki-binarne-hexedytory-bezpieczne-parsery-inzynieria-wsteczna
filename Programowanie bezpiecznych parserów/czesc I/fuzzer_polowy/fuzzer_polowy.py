import sys
import os
import subprocess


if len(sys.argv) < 3:
	sys.exit('usage: fuzzer_polowy.py <script> <sample> ')


script = sys.argv[1]
sample = sys.argv[2]
print(script, sample)

i = 0 
while True:
	i += 1
	output = subprocess.run([f'python3 {script} {sample}'], shell=True, check=True)
	if i == 1000:
		break
	else:
		print(f' ✓ {i}')	
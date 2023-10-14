import random
import sys


def read_bytes(f, n):  
    if f != n:
        raise Exception('Bytes do not match !!!')


if len(sys.argv) < 2:
	sys.exit('usage: prosty_mutator.py <fname>')

infile = sys.argv[1]
outfile = sys.argv[1] + '.mut'

f = bytearray(open(infile, 'rb').read())
len_f = len(f)
for i in range(0, len(f), 256):
	#f.append(1)
	random_offset = random.randint(0, 255)
	random_sz_bytes = random.randrange(1, 8, 1)
	#print(random_offset, random_sz_bytes)
	for j in range(i + random_offset, i + random_offset + random_sz_bytes):
		if j < len(f):
			f[j] = random.randint(0, 255) 
			#print(j)

read_bytes(len_f, len(f))
open(outfile, 'wb').write(f)	


# print(random_offset, random_nr_bytes, random_bytes_values)


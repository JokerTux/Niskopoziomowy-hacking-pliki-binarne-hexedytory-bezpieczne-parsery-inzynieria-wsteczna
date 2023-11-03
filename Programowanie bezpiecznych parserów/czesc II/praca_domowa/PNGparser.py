import struct
import sys


def resolution(f):
	total_bytes = len(f.read())
	f.seek(16)
	widht = f.read(4)
	widht = struct.unpack('>I', widht)[0]
	f.seek(20)
	height = f.read(4)
	height = struct.unpack('>I', height)[0]	
	return widht, height, total_bytes

def verification(f):
	f.seek(0)
	magic = f.read(8)
	if magic.hex() != '89504e470d0a1a0a':
		raise Exception('Unsupported file type !')

def chunk_info(f, total_bytes):
	current_pos = 8
	# 12 Bytes = 4B lenght, 4B name, 4B crc.
	_bytes = 12
	chunk_name_cmp = None
	for new_chunk in f:
		f.seek(current_pos)
		chunk = f.read(8)
		chunk_size, chunk_name = struct.unpack('>II', chunk)
		chunk_name = hex(chunk_name)
		chunk_name = bytearray.fromhex(chunk_name[2:]).decode('utf-8')
		print(f'chunk name = {chunk_name}, chunk size = {chunk_size} [B]')
		f.seek(current_pos)
		
		if chunk_name != chunk_name_cmp:
			buf = f.read(chunk_size + _bytes)[8:-4]
			with open(f'{chunk_name}.data', 'wb') as f_out:
				f_out.write(buf)
		else:
			buf = f.read(chunk_size + _bytes)[8:-4]	
			with open(f'{chunk_name}.data', 'ab') as f_out:
				f_out.write(buf)
						
		chunk_name_cmp = chunk_name		
		# print(buf)
		if chunk_name == 'IEND':
			break
		
		current_pos += chunk_size + _bytes

	

if __name__ == '__main__':

	if len(sys.argv) != 2:
		sys.exit('usage: PNGparser.py <file.png>')

	infile = sys.argv[1]
	
	with open(infile, 'rb') as f:
		verification(f)
		widht, height, total_bytes = resolution(f)
		chunk_info(f, total_bytes)

	print(f'widht = {widht}, height = {height}, bytes = {total_bytes}')

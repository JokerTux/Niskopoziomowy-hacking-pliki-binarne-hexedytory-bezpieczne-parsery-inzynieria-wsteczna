import struct
import sys


def verification(f):
	file_sz = len(f.read())

	f.seek(0)
	header_info = f.read(2)
	if header_info.hex() != '424d':
		raise Exception('Unsupported file type')
	
	f.seek(2)
	file_size = f.read(4)
	file_size = struct.unpack('<I', file_size)[0]
	if file_size != file_sz:
		print(file_size, file_sz)
		raise Exception('Declared bytes size is not equal to the actual file size')	

	f.seek(14)
	bmp_info_header = f.read(4)
	bmp_info_header = struct.unpack('<I', bmp_info_header)[0]
	if bmp_info_header != 40:
		raise Exception('BITMAPINFOHEADER != 40')	

	f.seek(28)
	color_depth = f.read(2)
	color_depth = struct.unpack('<H', color_depth)[0]
	if color_depth != 8:
		raise Exception('Unsupported .bmp type, "Color" was not declared [palette]')		
		
	f.seek(30)
	compression_method= f.read(4)
	compression_method = struct.unpack('<I', compression_method)[0]
	if compression_method != 1:
		raise Exception('Wrong compression method')

	f.seek(46)
	declared_colors_bin = f.read(4)
	declared_colors_bin = struct.unpack('<I', declared_colors_bin)[0]
	_check = 54 + (declared_colors_bin * 4) - 1
	f.seek(_check)
	byte_check = f.read(1)
	byte_check = struct.unpack('<B', byte_check)[0]
	if byte_check != 0:
		raise Exception('The color plaette is to long/short ')
		
	_check2 = _check + 1
	f.seek(_check2)
	data_sz = len(f.read())
	f.seek(34)
	data_lenght = f.read(4)
	data_lenght = struct.unpack('<I', data_lenght)[0]
	if (file_size - data_lenght) != _check2:
		raise Exception('Offset error')



def resolution(f):
	f.seek(18)
	width = f.read(4)
	width = struct.unpack('<I', width)[0]
	if width >= 10_000:
		raise Exception('width  > 10.000 px .')
	f.seek(22)
	height = f.read(4)
	height = struct.unpack('<I', height)[0]
	if height >= 10_000:
		raise Exception('height > 10.000 px .')
	print(f'BMP width = {width}, height = {height}')
	
	return width, height


def get_color(f):
	colors_hex_list = []
	bytes(colors_hex_list)
	f.seek(46)
	declared_colors = f.read(4)
	declared_colors = struct.unpack('<I', declared_colors)[0]
	declared_colors = declared_colors * 4 #Bytes for each color R G B 0 <- 0 end of line
	off_colors = 54
	f.seek(off_colors)
	colors_zs = f.read(declared_colors)
	if declared_colors == 0:
		raise Exception('No colors declared.')
	elif declared_colors >1 & declared_colors <=255:	
		for i in range(0, declared_colors, 4):
			f.seek(off_colors + i)
			color = f.read(3)[::-1]
			#print(color.hex())
			colors_hex_list.append(color)		
	else:
		raise Exception('Invalid palette size.')

	return colors_hex_list		


def get_rle(f):
	rle_bytes_list = []
	bytes(rle_bytes_list)
	f.seek(34)
	img_sz = f.read(4)
	img_sz = struct.unpack('<I', img_sz)[0]
	# print(img_sz)
	
	f.seek(10)
	rle_off = f.read(4)
	rle_off = struct.unpack('<I', rle_off)[0]
	f.seek(rle_off)

	if img_sz != 0:
		rle = f.read(img_sz)
		for i in rle:
			rle_bytes_list.append(i)
		# print(f'Declared bmp bytes = {rle}')
	else:
		raise Exception('Error,this file has no data')

	return rle		 


def export_file(width, height, rle_bytes, color_bytes_rgb):
	### RLE decompressed 
	indexes = []
	for i in range(0, len(rle_bytes), 2):
		j = i + 1
		a = rle_bytes[i]
		b = rle_bytes[j]
		for x in range(a):
			if a == 0 and b == 0 or a == 0 and b == 1:
				continue	
			indexes.append(b)
	#print(indexes)
	raw_colors = []
	for bytes_rle in indexes:
		raw_color = color_bytes_rgb[bytes_rle]
		raw_colors.append(raw_color)
	
	buf = b''	
	end_of_bytes_list = len(raw_colors)	* height
	# print(end_of_bytes_list)
	for scanline in range(end_of_bytes_list, 0, -(width)):
		end_of_bytes_list -= width
		if scanline <= width:
			end_of_bytes_list = 0
			scanline = width
			scanline = (scanline - 1)
			for by in raw_colors[scanline::-1][::-1]:
				buf += by
			break	
		for b in raw_colors[end_of_bytes_list:scanline]:
			buf += b

	with open(outfile, 'wb') as f_out:
		f_out.write(buf)	




if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('usage: parser_bmp_rle.py <file.bmp>')

	infile = sys.argv[1]
	outfile = sys.argv[1] + '.data'

	with open(infile, 'rb') as f:
		verification(f)
		width, height = resolution(f)	
		rle_bytes = get_rle(f)
		color_bytes_rgb = get_color(f)
		export_file(width, height, rle_bytes, color_bytes_rgb)
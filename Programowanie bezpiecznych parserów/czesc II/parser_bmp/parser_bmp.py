import struct
import sys


def bytes_bmp(f):
	f.seek(10)
	bmp_start_off = f.read(4)
	bmp_start_off = struct.unpack('<I', bmp_start_off)[0]
	return bmp_start_off

def bit_version_check(f):
	f.seek(28)
	#if color depth = 8, color palette is used.
	color_depth = f.read(2)
	color_depth = struct.unpack('<H', color_depth)[0]
	if color_depth == 8:
		print(f'BMB uses a color palette, color depth = {color_depth}')
		color_palette = colors(f)
	return color_palette

def colors(f):
	color_BGR_hex_val = []
	bytes(color_BGR_hex_val)
	f.seek(46)
	# if 0 = 256 colors-specification.
	color_fields = f.read(4)
	color_fields = struct.unpack('<I', color_fields)[0]

	if color_fields == 0:
		current_position = 54
		print('256 colors has been declared.')
		#0x400 = 1024 | 256 (colors) * 4 (bytes) = 1024
		for color_bytes in range(0, 0x400, 4):
			f.seek(current_position + color_bytes)
			# BGR to RGB
			color = f.read(3)[::-1]
			color_BGR_hex_val.append(color)
	
	#elif: other palettes with less colors : 
			
	else:
		raise Exception('This file has no color palette.')
	return color_BGR_hex_val

def export_file(f, data_size, outfile, start_off, color_palette):
	buf = b''
	test_list = []
	bytes(test_list)	
	for buff_val in range(start_off, data_size, 1):
		f.seek(buff_val)
		color_index = f.read(1)
		color_index = struct.unpack('<B', color_index)[0]
		# buf += color_palette[color_index]
		test_list.append(color_palette[color_index])		
	with open(outfile, 'wb') as f_out:
		for a in test_list:
			f_out.write(a)
	return f_out


if __name__ == '__main__':

	if len(sys.argv) < 2:
		sys.exit('usage: parser_bmp.py <file.bmp>')

	infile = sys.argv[1]
	outfile = sys.argv[1] + '.data'

	with open(infile, 'rb') as f:
		file_lenght = len(f.read())
		print(file_lenght)

		start_off = bytes_bmp(f)
		color_palette = bit_version_check(f)
		print(start_off)
		outfile = export_file(f, file_lenght, outfile, start_off, color_palette)
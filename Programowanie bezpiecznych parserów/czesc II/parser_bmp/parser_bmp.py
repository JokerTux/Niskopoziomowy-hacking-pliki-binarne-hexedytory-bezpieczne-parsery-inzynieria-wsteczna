import struct
import sys


def height_widht(f):
	max_lenght = 10000
	f.seek(18)
	width = f.read(4)
	width = struct.unpack('<I', width)[0]
	f.seek(22)
	height = f.read(4)
	height = struct.unpack('<I', height)[0]
	
	if width <= 0 or width > max_lenght:
		raise Exception('Invalid width')

	upside_down_flag = True
	if height == 0 or height >= max_lenght:
		raise Exception('Invalid height')
	if height < 0:
		upside_down_flag = False

	return width, height, upside_down_flag

def bytes_bmp(f):
	f.seek(10)
	bmp_start_off = f.read(4)
	bmp_start_off = struct.unpack('<I', bmp_start_off)[0]
	return bmp_start_off

def bit_version_check(f ,file_lenght):
	f.seek(0)
	header_info = f.read(2)
	if header_info.hex() != '424d':
		raise Exception('Unsupported file type')

	f.seek(2)
	file_size = f.read(4)
	file_size = struct.unpack('<I', file_size)[0]
	if file_size != file_lenght:
		print(file_size, file_lenght)
		raise Exception('Declared bytes size is not equal to the actual file size')	

	f.seek(14)
	bmp_info_header = f.read(4)
	bmp_info_header = struct.unpack('<I', bmp_info_header)[0]
	if bmp_info_header != 40:
		raise Exception('BITMAPINFOHEADER != 40')

	f.seek(30)
	compression_method= f.read(4)
	compression_method = struct.unpack('<I', compression_method)[0]
	if compression_method != 0:
		raise Exception('Wrong compression method')		
		
	f.seek(28)
	#if color depth = 8, color palette is used.
	color_depth = f.read(2)
	color_depth = struct.unpack('<H', color_depth)[0]
	if color_depth == 8:
		print(f'BMP uses a color palette, color depth = {color_depth}')
		color_palette = colors(f)
	return color_palette

def colors(f):
	color_BGR_hex_val = []
	bytes(color_BGR_hex_val)
	f.seek(46)
	# if 0 = 256 colors-specification.
	color_fields = f.read(4)
	color_fields = struct.unpack('<I', color_fields)[0]
	current_position = 54

	if color_fields == 0:
		print('256 colors has been declared.')
		#0x400 = 1024 | 256 (colors) * 4 (bytes)= 1024. 3x hex values and 0 acts like \n
		for color_bytes in range(0, 0x400, 4):
			f.seek(current_position + color_bytes)
			# BGR to RGB
			color = f.read(3)[::-1]
			color_BGR_hex_val.append(color)

	elif color_fields >= 1 and color_fields <= 255:
		print(f'{color_fields} colors has been declared')
		color_fields = color_fields * 4
		for color_bytes in range(0, color_fields, 4):
			f.seek(current_position + color_bytes)
			# BGR to RGB
			color = f.read(3)[::-1]
			color_BGR_hex_val.append(color)
	else:
		raise Exception('Invalid palette size.')	
	return color_BGR_hex_val

def export_file(f, data_size, outfile, start_off, color_palette, width, upside_down_flag):
	buf = b''
	test_list = []
	bytes(test_list)

	scanline_w = width
	if width % 4:
		scanline_w = 4 -(scanline_w % 4)
		_a = width + scanline_w
		for byte_val in range(start_off,data_size, _a):
			f.seek(byte_val)
			indexes = f.read(width)
			for index in indexes:
				test_list.append(color_palette[index])		
	else:
		for buff_val in range(start_off, data_size, 1):
			f.seek(buff_val)
			color_index = f.read(1)
			color_index = struct.unpack('<B', color_index)[0]
			test_list.append(color_palette[color_index])

	# loading the scanlines upside down
	if upside_down_flag == True:
		step = width #file width 
		end_of_bytes_list = len(test_list)
		for scanline in range(end_of_bytes_list, 0, -(step)):
			end_of_bytes_list -= step
			if scanline <= step :
				end_of_bytes_list = 0
				scanline = width
				scanline = (scanline - 1)
				for by in test_list[scanline::-1][::-1]:
					buf += by
				break
			for b in test_list[end_of_bytes_list:scanline]:
				buf += b

		new_size = len(buf)
		with open(outfile, 'wb') as f_out:
			f_out.write(buf)
	else:
		print(test_list)		
	return f_out, new_size


if __name__ == '__main__':

	if len(sys.argv) != 2:
		sys.exit('usage: parser_bmp.py <file.bmp>')

	infile = sys.argv[1]
	outfile = sys.argv[1] + '.data'

	with open(infile, 'rb') as f:
		file_lenght = len(f.read())
		color_palette = bit_version_check(f, file_lenght)
		start_off = bytes_bmp(f)
		width, height, upside_down_flag = height_widht(f)
		outfile, new_size = export_file(f, file_lenght, outfile, start_off, color_palette, width, upside_down_flag)
		print(f'{file_lenght} [bytes] file size, {width} width, {height} height, {new_size} [bytes] new file size.')
		sys.exit(0)
from os import walk


def read_bytes(f, n):
    
    if f != n:
        raise Exception('Bytes do not match !!!')
    return n


total_files = []
for path, subdirs, files in walk('/home/remnux/Downloads/day3/day1/splitflag'):
    for file in files:
        total_files.append(file)        
                  
buf = b''
total_files.sort() 
print(total_files)
for file_bin in total_files:
    mish_mash_path = f'/home/remnux/Downloads/day3/day1/splitflag/{file_bin}'
    #1st offset 0x123 = 291(d) 10B, 2nd offset 0xabc = 2748(d) 10B, 3rd offset -10 5B.
    with open(mish_mash_path, 'rb') as f:
        f.seek(291)
        buf += f.read(10)
        f.seek(0)
        f.seek(2748)
        buf += f.read(10)
        f.seek(0)
        f.seek(-10, 2)
        buf += f.read(5)
        #print(third_offset.hex(), f.tell())
        with open('my_png.png', 'wb') as new_f:
            new_f.write(buf)
            #new_f.write(first_offset + second_offset + third_offset)
        #print(first_offset.hex(), second_offset.hex(), third_offset.hex())



with open('my_png.png', 'rb') as f:
    f = len(f.read())
    n = len(buf)
    print(f)
    read_bytes(f, n)

#f = open('spec1_1.bin', 'rb')
#print(f.read())

#f.read(1092)
#print(f.read())
#i = f.tell()
#print(i)

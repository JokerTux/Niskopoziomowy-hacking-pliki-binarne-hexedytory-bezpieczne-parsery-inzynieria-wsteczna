from sys import getsizeof
from os import walk


total_files = []
for path, subdirs, files in walk('/home/remnux/Downloads/day3/day1/splitflag'):
    for file in files:
        total_files.append(file)        
                  

total_files.sort() 
print(total_files)
for file_bin in total_files:
    mish_mash_path = f'/home/remnux/Downloads/day3/day1/splitflag/{file_bin}'
    #1st offset 0x123 = 291(d) 10B, 2nd offset 0xabc = 2748(d) 10B, 3rd offset -10 5B.
    with open(mish_mash_path, 'rb') as f:
        first_offset = f.seek(291)
        first_offset = f.read(10)
        second_offset = f.seek(0)
        second_offset = f.seek(2748)
        second_offset = f.read(10)
        third_offset = f.seek(0)
        third_offset = f.seek(-10, 2)
        third_offset = f.read(5)
        #print(third_offset.hex(), f.tell())
        with open('my_png.png', 'ab') as new_f:
            new_f.write(first_offset + second_offset + third_offset)
        print(first_offset.hex(), second_offset.hex(), third_offset.hex())

#f = open('spec1_1.bin', 'rb')
#print(f.read())

#f.read(1092)
#print(f.read())
#i = f.tell()
#print(i)

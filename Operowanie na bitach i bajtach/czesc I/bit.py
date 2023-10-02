from bitarray import bitarray


def create_mask(a):
    print(a)

    i = 8
    j = 0
    bits_found = []

    for bit in a:
        i -= 1
        if bit == 1:
            j += 1
            bits_found.append(i)
            
    #shift_left = int(bits_found[-1])
    #bit_fields_bits = int(j)
    
    shift_left = input('how many fields do you want to shift left ? ' )
    bit_fields_bits = input('how many bit fileds do we need ? ')

    mask = ((1 << int(bit_fields_bits)) - 1)
    mask = mask << int(shift_left)

    print(mask)
    mask_bin = '{0:08b}'.format(mask)
    print(mask_bin)
    print(hex(mask))
    print('-------------------------------------------')
    
    return mask_bin, shift_left, bit_fields_bits


def AND_on_mask(mask, a, shift_left, bit_fields_bits):

    print('Original Byte : ', a)    
    bits_mask = bitarray(mask)
    result = a & bits_mask
    print('AND operation result : ', result)
    ## Moving the extracted bits to the right side 
    moving_right = ((1 >> int(bit_fields_bits)) - 1)
    moving_right = result >> int(shift_left) 
    print(moving_right)
    decimal_result = int(moving_right.to01(), base = 2)
    print('Decimal value : ', decimal_result)
    print('------------------------------------------')

def OR_bits_replace(mask, a, shift_left, bit_fields_bits):
    print('Original Byte : ', a) 
    #breakpoint()
    
    #my_bits = bitarray('0000 1100')
    my_bits = 0b101 
    #my_bits = bin(my_bits)
    my_bits = '{0:08b}'.format(my_bits)   
    my_bits = bitarray(my_bits)
    #print(type(my_bits))
    print('Payload : ', my_bits)
    

    or_mask = bitarray(mask)
    or_mask = ~or_mask
    print('OR mask', or_mask)
    result = a & or_mask
    print('result of clearing bits : ', result)
    
  
    my_bits = my_bits << int(shift_left)
    #print('crap... ', payload_move_left)
    #breakpoint()
    a = result | my_bits
    print(a)

a = bitarray('1000 1111')
mask_bin, shift_left, bit_fields_bits = create_mask(a)
AND_on_mask(mask_bin, a, shift_left, bit_fields_bits)
OR_bits_replace(mask_bin, a, shift_left, bit_fields_bits)
#b = bitarray('0000 0111')
#create_mask(b)
#c = bitarray('0001 0000')
#create_mask(c)


        
#print('bit fields =', j)
#print('spaces to shift left', bits_found[-1])

#print(a, b, len(c))

from pylz78.ctrie import CTrie

def encodeLZ78(inputfile, filename, n_bytes_index, n_bytes_character):
    with open(inputfile, 'r') as file:
        text = file.read()
    with open(filename, 'wb') as file:

        D = CTrie('', numeric_value=0)
        cadeia = ''
        i = 1
        for c in text:
            value = D.contains(cadeia + c)
            if value != -1:
                cadeia += c
            else:
                value_of_cadeia = D.contains(cadeia)
                file.write(value_of_cadeia.to_bytes(n_bytes_index, "big"))
                file.write(ord(c).to_bytes(n_bytes_character, "big"))
                D.add(cadeia + c, i) 
                i += 1
                cadeia = ''

        file.write((D.contains(cadeia)).to_bytes(3, byteorder="big"))

def decodeLZ78(filename, inputfile, n_bytes_index, n_bytes_character):
    D = ['']
    decoded = ''
    with open(filename, 'rb') as file:
        while True :
            index = file.read(n_bytes_index)
            if index == b'':
                break
            index = int.from_bytes(index, byteorder="big")
            c = file.read(n_bytes_character)
            if c == b'':
                c = ''
            else:
                c = chr(int.from_bytes(c, byteorder="big"))
            cadeia = D[index]
            decoded += cadeia + c
            D += [cadeia + c]
            
    with open(inputfile, 'w') as file:
        file.write(decoded)
        



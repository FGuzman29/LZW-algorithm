import sys, re, os, io, base64, pickle
from io import StringIO

dictionary_size = 256
compression_results = [] #lista de listas, donde indice [0][0] es el nombre del primer archivo comprimido y el resto es la lista de enteros resulatado de la compresion 

def compression(inputFile):
    counter = 256
    compresCharTable = dict((chr(j), j) for j in range(counter))
    result = []
    p = ''
    
    for byte in inputFile:
        pc = p + byte
        if pc in compresCharTable:
            p = pc
        else:
            result.append(compresCharTable[p])
            compresCharTable[pc] = counter
            counter += 1
            p = byte
    if p:
        result.append(compresCharTable[p])
    return result
        
def write_result(name,result):
    global compression_results
    result.insert(0,name)
    compression_results += (result,)


def save_comp_file():
    global compression_results
    outfile = open('result.lzw','wb')
    pickle.dump(compression_results,outfile)    

def decompress(compressed): #from rosetta code
    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)
 
        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
 
        w = entry
    return result.getvalue()
    

def iterate_and_compress(arguments):
    for arg in arguments:
        if os.path.isfile(arg): #if argument is a file opens and compressess it
            with open(arg,'r') as f:
                write_result(arg, compression(f.read())) 
                #agregar condicional si es imagen
                
                
        else: #if it's a directory scans and iterates it's paths
            for entry in os.scandir(arg):
                if entry.path.endswith(".txt"):
                    with open(entry.path,'rb') as f: 
                        write_result(entry.path, compression(f.read().decode()))
                        
                        
                if entry.path.endswith(".png") or entry.path.endswith(".jpg"):
                    with open(entry.path,'rb') as f:
                        img = base64.b64encode(f.read())
                        
                        write_result(entry.path, compression(img.decode('utf-8')))                      
    save_comp_file()
                                
def decompress_and_iterate(file_path):
    
    with open(file_path, 'rb') as lzw_file:
        compressed_files = pickle.load(lzw_file)
        
        for file in compressed_files:
            file_name = file.pop(0)
            result = decompress(file)
            
            if file_name.endswith('.txt'):
                new_file = open(file_name,'w')
                
                
            elif file_name.endswith('.png') or file_name.endswith('.jpg'):
                new_file = open(file_name,'wb')
                result = base64.b64decode(result)

            new_file.write(result)
            new_file.close()

def main():
        
    arguments = sys.argv[1:]  #saves arguments and removes the first one(which is *.py)

    try:
        if arguments[0] == '-c':
            iterate_and_compress(arguments[1:]) #pass remaining arguments
                    
        elif arguments[0] == '-d':
            decompress_and_iterate(arguments[1])
                
        elif arguments[0] == ("-h"): 
                print('COMMANDS: \n compress mode: -c followed by as many files and directories as you want \n decompress mode: -d followed by a single .lzw file')
    
    except IndexError:
        print('no arguments found')    
    
if __name__ == "__main__":
    main()
    
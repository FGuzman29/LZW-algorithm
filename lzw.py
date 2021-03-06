#! /usr/bin/python3
import sys, re, os, io, base64, pickle
from io import StringIO

dictionary_size = 256
compressed_files = [] #lista de listas, donde indice [0][0] es el nombre del primer archivo comprimido y el resto es la lista de enteros resulatado de la compresion 

def compression(inputFile):#in: string  out:list of ints
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
    global compressed_files
    result.insert(0,name)
    compressed_files += (result,)


def save_comp_file():
    global compressed_files
    outfile = open('result.lzw','wb')
    pickle.dump(compressed_files,outfile)    

def decompress(compressed): #in: list of ints   out:string
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
        
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
 
        w = entry
    return result.getvalue()
    

def filter(file_path):
    if ('.png' in file_path.lower()) or ('.jpg' in file_path.lower()):
    #if file_path.lower().endswith(".png") or file_path.lower().endswith(".jpg"): #si es imagen la codifica a base64 y luego decodifica a string(utf-8) para usar en alg de compresion
        with open(file_path,'rb') as f:
            name = os.path.basename(file_path)
            img = base64.b64encode(f.read())
            write_result(name, compression(img.decode('utf-8')))
            
    else: #cualquier otro archive asume que contiene texto (.txt, .c)
        with open(file_path,'r') as f: 
            name = os.path.basename(file_path)
            write_result(name, compression(f.read()))
                               
    save_comp_file()
    
def argument_iterator(arguments):
    for arg in arguments: 
        if os.path.isfile(arg): 
            filter(arg)
            
        else:
            for entry in os.scandir(arg):
                filter(os.path.join(arg,entry.name))
                                
def decompress_and_iterate(file_path):
    global compressed_files
    with open(file_path, 'rb') as lzw_file: #open .lzw file
        compressed_files = pickle.load(lzw_file)
        
        for file in compressed_files:
            file_name = file.pop(0)
            result = decompress(file)
            dir_name = os.path.dirname(file_name)
            if dir_name != "":
                os.makedirs(dir_name,exist_ok=True)
                
            if ('.png' in file_name.lower()) or ('.jpg' in file_name.lower()):             
            #if file_name.endswith('.PNG') or file_name.endswith('.JPG'):
                new_file = open(file_name,'wb')
                result = base64.b64decode(result)
            else:
                new_file = open(file_name,'w')
            new_file.write(result)
            new_file.close()

def main():
    sys.getdefaultencoding()
    arguments = sys.argv[1:]  #saves arguments and removes the first one(which is *.py)

    try:
        if arguments[0] == '-c':
            argument_iterator(arguments[1:]) #pass remaining arguments
                    
        elif arguments[0] == '-d':
            decompress_and_iterate(arguments[1])
                
        elif arguments[0] == ("-h"): 
            print('Flags: \n compress mode: -c  \n decompress mode: -d\n help: -h')
            print("Usage: \nTo compress\n Windows: lzw.py [-c] [files/directories ToCompress list]")
            print(" Linux:python3 lzw.py [-c] [files/directories ToCompress list] ")
            print("To decompress\n Windows: lzw.py [-d] [filesToDecompress]")
            print(" Linux:python3 lzw.py [-d] [filesToDecompress]")
    
    except IndexError:
        print('no arguments found')    
    
if __name__ == "__main__":
    main()
    
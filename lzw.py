import sys, re, os, io, base64, pickle
from io import StringIO

dictionary_size = 256

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

def writeResult(name,result):
    outputFile = open("file.lzw","w")
    outputFile.write(name + " ")
    for i  in result:
        outputFile.write(str(i) + " ")
        
def writeResult2 (result):
    outfile = open('result.lzw','wb')
    pickle.dump(result,outfile)
    
def convertToInt(inputFile):
    aux = []
    for i in inputFile:
        aux.append(int(i))
    return  aux

def decompress(inputFile):
    global counter,decomCharTable
    decomCharTable =  dict((j, chr(j)) for j in range(counter))
    
    inputFile = inputFile.split()
    fileName = inputFile.pop(0)
    inputFile = convertToInt(inputFile)
    p = chr(inputFile.pop(0))
    outputFile = open(fileName,"wb")
    outputFile.write(p)

    for c in inputFile:
        if c  in decomCharTable:
            entry = decomCharTable[c]
            
        elif c == counter:
            entry = p + p[0]
        outputFile.write(entry)
        decomCharTable[counter] = p + entry[0]
        counter += 1
        p = entry
    outputFile.close()


def decompress3(compressed): #from rosetta code
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
                    with open(arg,'rb') as f:
                        # b64string = base64.b64encode(f.read())
                        # print(b64string)
                        # print(type(b64string))
                        # print(f.read().decode())
                        writeResult2(compression(f.read().decode()))
                        
                        
                else: #if it's a directory scans and iterates it's paths
                    for entry in os.scandir(arg):
                        if (entry.path.endswith(".txt") or entry.path.endswith(".png")) and entry.is_file():
                            with open(entry.path,'r') as f:
                                print(compression(f.read()))
                                
def decompress_and_iterate(file_path): #just one file for now

    with open(file_path, 'rb') as infile:
        content = pickle.load(infile)
        print(decompress3(content))

def main():
        
    arguments = sys.argv[1:]  #saves arguments and removes the first one(which is *.py)

    try:
        if arguments[0] == '-c':
            iterate_and_compress(arguments[1:]) #pass remaining arguments
                    
        elif arguments[0] == '-d':
            decompress_and_iterate(arguments[1])
            # with open(arguments[1]) as f:
            #     decompress(f.read())
                
        elif arguments[0] == ("-h"): 
                print('COMMANDS: \n compress mode: -c followed by as many files and directories as you want \n decompress mode: -d followed by a single .lzw file')
    
    except IndexError:
        print('no arguments found')    
    
if __name__ == "__main__":
    main()
            
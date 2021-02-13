import getopt, sys, re
import os
import io
counter = 256
compresCharTable = dict((chr(j), j) for j in range(counter)) 
decomCharTable =  dict((j, chr(j)) for j in range(counter))

def compression(inputFile):
    global counter,compresCharTable
    result = []
    p = ""
    i = 0
    while i < len(inputFile):
        c = chr(inputFile[i])
        pc = p + c
        if pc in compresCharTable:
            p = pc
        else:
            result.append(compresCharTable[p])
            compresCharTable[pc] = counter
            counter += 1
            p = c
        i += 1
    
    if p:
        result.append(compresCharTable[p])
    return result

def writeResult(name,result):
    outputFile = open("file.lzw","w")
    outputFile.write(name + " ")
    for i  in result:
        outputFile.write(str(i) + " ")
    
def convertToInt(inputFile):
    aux = []
    for i in inputFile:
        aux.append(int(i))
    return  aux

def decompress(inputFile):
    global counter,decomCharTable
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
    
    

def iterate_and_compress(arguments):
    for arg in arguments:
                if os.path.isfile(arg): #if argument is a file opens and compressess it
                    with open(arg,'r') as f:
                        print(compression(f.read()))
                        
                else: #if it's a directory scans and iterates it's paths
                    for entry in os.scandir(arg):
                        if (entry.path.endswith(".txt") or entry.path.endswith(".png")) and entry.is_file():
                            with open(entry.path,'r') as f:
                                print(compression(f.read()))

def main():
        
    arguments = sys.argv[1:]  # guarda los argumentos y quita el primero(que es *.py)

    try:
        if arguments[0] == '-c':
            #place old here
            iterate_and_compress(arguments[1:]) #pass remaining arguments
                    
        elif arguments[0] == '-d':
            with open(arguments[1]) as f:
                decompress(f.read())
                
        elif arguments[0] == ("-h"): 
                print('COMMANDS: \n compress mode: -c followed by as many files and directories as you want \n decompress mode: -d followed by a single .lzw file')
    
    except IndexError:
        print('no arguments found')    
    
if __name__ == "__main__":
    main()
            
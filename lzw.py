import getopt, sys, re
import os, io
import base64
counter = 256
compresTable = dict((chr(j), j) for j in range(counter)) 
decompressTable = dict((j,chr(j)) for j in range(counter))
def compression(inputFile):
    global counter,compresTable
    result = []
    p = ""

    for c in inputFile:
        if type(c) == int:
            c = chr(c)
        
        pc = p + c
        if pc in compresTable:
            p = pc

        else:
            result.append(compresTable[p])
            compresTable[pc] = counter
            counter +=1
            p = c

    if p:
        result.append(compresTable[p])

    return result

def writeResult(name, result):
    outputFile = open("file.lzw","w")
    outputFile.write(name + " ")

    for i in result:
        outputFile.write(str(i) + " ")

    outputFile.close()

def decompression(inputFile):
    global counter, decompressTable
    inputFile = inputFile.split() #split the string into a list
    fileName = inputFile.pop(0) #save the file name and delete it from the list
    inputFile = convertToInt(inputFile)
    result = ""
    p = chr(inputFile[0])
    result += p
    i = 1

    while i < len(inputFile):
        c = inputFile[i]

        if c not in decompressTable:
            s = p + p[0]

        else:
            s = decompressTable[c]

        result += s
        decompressTable[counter] = p + s[0]
        counter += 1
        p = s
        i += 1
    
    if ".PNG" in fileName or ".JPG" in fileName: #if file is an image, write it in bytes
        outputFile = open(fileName ,"wb")
        result = base64.b64decode(result)

    else: 
        outputFile = open(fileName, "w")
        
    outputFile.write(result) 
    outputFile.close()

def convertToInt(arr):
    aux = []

    for i in arr:
        aux.append(int(i))

    return aux

def mainTest():
    selection = input("c for compression, d for decompresion: ")
    if selection == 'c':
        path = input("Add path: ")
        inputFile = io.open(path,"rb")
        fileName = os.path.basename(path)

        if ".PNG" in fileName or ".JPG" in fileName:
            img = base64.b64encode(inputFile.read())
            result = compression(img)

        else:
            result = compression(inputFile.read())

        writeResult(fileName,result)

    if selection == 'd':
        path = input("Add path: ")
        inputFile = io.open(path,"r")
        result = decompression(inputFile.read())
    
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
            
import sys, re, os, io, base64, pickle

compression_results = [] #lista de listas, donde indice [0][0] es el nombre del primer archivo comprimido y el resto es la lista de enteros resulatado de la compresion 

def compression(inputFile):
    counter = 256
    compresTable = dict((chr(j), j) for j in range(counter))     
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
        
def write_result(name,result):
    global compression_results
    result.insert(0,name)
    compression_results += (result,)


def save_comp_file(path):
    global compression_results
    outfile = open(path+".lzw",'w')
    for i in compression_results:
        for j in i:
            outfile.write(str(j) + " ")
        outfile.write("\n")
    outfile.close()
    

def decompress(compressed):
    counter = 256
    decompressTable = dict((j,chr(j)) for j in range(counter))
    compressed = compressed.split()
    fileName = compressed.pop(0)
    compressed = convertToInt(compressed)
    result = ""
    p = chr(compressed[0])
    result += p
    i = 1
    while i < len(compressed):
        c = compressed[i]
        if c not in decompressTable:
            s = p + p[0]
        else:
            s = decompressTable[c]
        result += s
        decompressTable[counter] = p + s[0]
        counter += 1
        p = s
        i += 1
    
    if ".png" in fileName.lower() or ".jpg" in fileName.lower():
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
    
def iterate_and_compress(arguments):
    final = arguments.pop()
    for arg in arguments:
        if os.path.isfile(arg): #if argument is a file opens and compressess it
            f = open(arg,"rb")
            name = os.path.basename(arg)
            if ".png" in name.lower() or ".jpg" in name.lower():
                img = base64.b64encode(f.read())
                write_result(name, compression(img))
            else:
                write_result(name, compression(f.read()))

    save_comp_file(final)
                                
def decompress_and_iterate(file_path):
    
    with open(file_path, 'r') as lzw_file:
        compressed_files = lzw_file.readlines()
        for inputFile in compressed_files:
            decompress(inputFile)


def main():
        
    arguments = sys.argv[1:]  #saves arguments and removes the first one(which is *.py)

    try:
        if arguments[0] == '-c':
            iterate_and_compress(arguments[1:]) #pass remaining arguments
                    
        elif arguments[0] == '-d':
            decompress_and_iterate(arguments[1])
                
        elif arguments[0] == ("-h"): 
                print('Flags: \n compress mode: -c  \n decompress mode: -d\n help: -h')
                print("Usage: \n Windows: lzw.py [-mode/flag] [filesToCompress list] [compressedFile]")
                print(" Linux:python3 lzw.py [-mode/flag] [filesToCompress list] [compressedFile]")
                print("Warning: \n Last")
    
    except IndexError:
        print('no arguments found')    
    
if __name__ == "__main__":
    main()
    
import getopt, sys, re
import os

counter = 256
charTable = {}

def compression(inputFile):
    global counter,charTable
    charTable = dict((chr(j), j) for j in range(counter))
    result = []
    p = ""
    for c in inputFile:
        pc = p + c
        if pc in charTable:
            p = pc
        else:
            result.append(charTable[p])
            charTable[pc] = counter
            counter += 1
            p = c
    return result

def decompress(object):
    print("dosoemthing")

def iterate_and_compress(arguments):
    for arg in arguments:
                if os.path.isfile(arg): #if argument is a file opens and compressess it
                    with open(arg) as f:
                        print(compression(f.read()))
                        
                else: #if it's a directory scans and iterates it's paths
                    for entry in os.scandir(arg):
                        if (entry.path.endswith(".txt") or entry.path.endswith(".png")) and entry.is_file():
                            print(entry.path)

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
            
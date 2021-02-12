#!/usr/bin/env python
import getopt, sys, re
from os import path

counter = 256
charTable = {}

def compression(inputFile):
    i = 0
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

def main():
        # quita el primer argumento (que es *.py)
    arguments = sys.argv[1:]
    
    # definicion de los flags
    options = "c:d:h:"

    try:
        # Parsing argument
        arguments, values = getopt.getopt(arguments, options)
        
        # checking each argument
        for current_argument, current_value in arguments:
            
            if current_argument in ("-c"): 
                #print(compression("WYS*WYGWYS*WYSWYSG"))        
                with open(current_value) as f:
                    compression(f.read())

            elif current_argument in ("-d"):   
                decompress(current_value)
            
            elif current_argument in ("-h"): 
                print('COMMANDS: \n compress mode: -c followed by as many files and directories as you want \n decompress mode: -d followed by a single .lzw file')
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))

    if arguments[0] not in("-c","-d","-h"):
                print(arguments[0])
            
            
            
            
if __name__ == "__main__":
    main()
            
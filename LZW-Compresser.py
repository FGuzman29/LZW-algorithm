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

def main():
    print(compression("WYS*WYGWYS*WYSWYSG"))

main()
            
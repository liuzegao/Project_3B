#!/usr/local/cs/bin/python3
# NAME: Zegao Liu
# EMAIL: liuzegao2012@gmail.com
# ID: 004189106

import sys



def ScanData(file):
    #csv_content = [line.strip() for line in file]

    for line in file:
        fileLineFields = line.split(",")
        #csv_dict[fileLineFields[0]].append(fileLineFields)
        if fileLineFields[0] == "SUPERBLOCK":
            global inodeSize
            inodeSize = int(fileLineFields[4])
            global blockSize
            blockSize = int(fileLineFields[3])
        if fileLineFields[0] == "GROUP":
            global firstInodeBlock
            firstInodeBlock = int(fileLineFields[8])







def main():
    if len(sys.argv) != 2:
        print("Invalid Argument")
        sys.exit(1)

    with open(str(sys.argv[1]), "r") as file:
        ScanData(file.readlines())



if __name__ == "__main__":
    main()
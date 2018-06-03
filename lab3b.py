#!/usr/local/cs/bin
# NAME: Zegao Liu
# EMAIL: liuzegao2012@gmail.com
# ID: 004189106

import sys
from collections import defaultdict


freeList = {}
allocated = {}
markedlinkCount = {}
realLinkCount = defaultdict(int)
unallocatedLinkCount = {}
direntChildName = {}
direntChildInode = {}
realParentNode = {}

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
            global firstInode
            firstInode = int(fileLineFields[7])
        if fileLineFields[0] == "GROUP":
            global blockNum
            blockNum = int(fileLineFields[2])
            global inodeNum
            inodeNum = int(fileLineFields[3])
            inodeTableOffset = int(fileLineFields[8].split('\n')[0])
        if fileLineFields[0] == "IFREE":
            inodeIndex = int(fileLineFields[1])
            freeList[inodeIndex] = 1
            #print(inodeIndex)
        if fileLineFields[0] == "INODE":
            inodeIndex = int(fileLineFields[1])
            allocated[inodeIndex] = 1
            markedlinkCount[inodeIndex] = int(fileLineFields[6])
        if fileLineFields[0] == "DIRENT":
            if fileLineFields[1] not in direntChildInode.keys():
                direntChildInode[fileLineFields[1]] = []
                direntChildInode[fileLineFields[1]].append((int(fileLineFields[3]),fileLineFields[6].split('\n')[0],int(fileLineFields[3])))
            else:
                direntChildInode[fileLineFields[1]].append((int(fileLineFields[3]), fileLineFields[6].split('\n')[0],int(fileLineFields[3])))

            if fileLineFields[6].split('\n')[0] == "'..'" and int(fileLineFields[1]) == 2 :
                realParentNode[int(fileLineFields[3])] = 2

            if fileLineFields[6].split('\n')[0] != "'..'" and fileLineFields[6].split('\n')[0] != "'.'":
                realParentNode[int(fileLineFields[3])] = int(fileLineFields[1])
            realLinkCount[int(fileLineFields[3])] += 1

    global firstBlock
    #print(realParentNode)
    firstBlock = inodeTableOffset + (inodeSize * inodeNum / blockSize)

    #print(allocated)

def checkInode():
    for key in freeList.keys():
        if (key in allocated.keys()):
            print("ALLOCATED INODE {0} ON FREELIST".format(key))

    for i in range(firstInode, inodeNum + 1):
        if (i not in freeList) and (i not in allocated):
            print('UNALLOCATED INODE ' + str(i) + ' NOT ON FREELIST')
            unallocatedLinkCount[i] = 1

    for key,value in markedlinkCount.items():
        if(key in realLinkCount.keys()):
            if(realLinkCount[key]==value):
                continue
        else:
            print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, markedlinkCount[key], 0))
            continue
        print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, markedlinkCount[key], realLinkCount[key]))

    for key, value in unallocatedLinkCount.items():
        if (key in realLinkCount.keys()):
            print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, 0, realLinkCount[key]))

    for key, value in direntChildInode.items():
        for i in value:
            if i[0] < 1 or i[0] > inodeNum:
                print("DIRECTORY INODE {0} NAME {1} INVALID INODE {2}".format(key, i[1], i[0]))
            elif(i[0] in unallocatedLinkCount.keys()):
                print("DIRECTORY INODE {0} NAME {1} UNALLOCATED INODE {2}".format(key, i[1], i[0]))

            if i[1] == "'..'":
                if int(key) in realParentNode.keys():
                    if realParentNode[int(key)] != i[2]:
                        print("DIRECTORY INODE {0} NAME '..' LINK TO INODE {1} SHOULD BE {2}".format(key, i[2],realParentNode[int(key)]))

            if i[1] == "'.'":
                if int(key) != i[0]:
                    print("DIRECTORY INODE {0} NAME '.' LINK TO INODE {1} SHOULD BE {0}".format(key, i[0]))


def main():
    if len(sys.argv) != 2:
        print("Invalid Argument")
        sys.exit(1)

    with open(str(sys.argv[1]), "r") as file:
        ScanData(file.readlines())

    checkInode()

if __name__ == "__main__":
    main()
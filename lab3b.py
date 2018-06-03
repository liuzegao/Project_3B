<<<<<<< HEAD
#!/usr/local/cs/bin
# NAME: Zegao Liu
# EMAIL: liuzegao2012@gmail.com
# ID: 004189106
=======
#!/usr/local/cs/bin/python
#NAME: Zegao Liu,Jiayu Zhao
#EMAIL: liuzegao2012@gmail.com,jyzhao1230@g.ucla.edu
#ID: 004189106,904818173
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8

import sys
from collections import defaultdict

inconsistencies = 0

freeList = {}
allocated = {}
markedlinkCount = {}
realLinkCount = defaultdict(int)
unallocatedLinkCount = {}
direntChildName = {}
direntChildInode = {}
realParentNode = {}

<<<<<<< HEAD
def ScanData(file):
    #csv_content = [line.strip() for line in file]
    for line in file:
=======
block_freelist = {}
block_allocationlist = {}

def ScanData(my_file):
    #csv_content = [line.strip() for line in file]
    for line in my_file:
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
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

<<<<<<< HEAD
    #print(allocated)
=======
def offset_calc(field_num):
    #direct fields
    index = field_num - 12
    if index >= 0 and index <= 11:
        return index
    elif index == 12:
        return index
    elif index == 13:
        return 12 + 256
    elif index == 14:
        return 12 + 256 + 256*256
    

def create_blockdic(my_file1):
    for lines in my_file1:
        fileLineFields = lines.split(",")
        if fileLineFields[0] == "INODE":
            if fileLineFields[2] != "s":
                for i in range(12,27):
                    my_block_num = int(fileLineFields[i])
                    if my_block_num < 0 or my_block_num > blockNum:
                        inconsistencies = 1
                        my_offset = offset_calc(i)
                        message = " " + str(my_block_num) + " IN INODE " + fileLineFields[1] + " AT OFFSET " + str(my_offset)
                        if i >= 12 and i <= 23:
                            print("INVALID BLOCK" + message)
                        elif i == 24:
                            print("INVALID INDIRECT BLOCK" + message)
                        elif i == 25:
                            print("INVALID DOUBLE INDIRECT BLOCK" + message)
                        elif i == 26:
                            print("INVALID TRIPLE INDIRECT BLOCK" + message)
                    elif my_block_num > 0 and my_block_num < firstBlock:
                        inconsistencies = 1
                        my_offset = offset_calc(i)
                        message = " " + str(my_block_num) + " IN INODE " + fileLineFields[1] + " AT OFFSET " + str(my_offset)
                        if i >= 12 and i <= 23:
                            print("RESERVED BLOCK" + message)
                        elif i == 24:
                            print("RESERVED INDIRECT BLOCK" + message)
                        elif i == 25:
                            print("RESERVED DOUBLE INDIRECT BLOCK" + message)
                        elif i == 26:
                            print("RESERVED TRIPLE INDIRECT BLOCK" + message)
                    else:
                        if my_block_num > 0:
                            if my_block_num not in block_allocationlist:
                                block_allocationlist[my_block_num] = []
                                block_allocationlist[my_block_num].append((my_block_num, int(fileLineFields[1]), i, offset_calc(i)))
                            else:
                                block_allocationlist[my_block_num].append((my_block_num, int(fileLineFields[1]), i, offset_calc(i)))
        if fileLineFields[0] == "BFREE":
            my_block_num = int(fileLineFields[1])
            block_freelist[my_block_num] = True
        if fileLineFields[0] == "INDIRECT":
            my_block_num = int(fileLineFields[5])
            if my_block_num < 0 or my_block_num > blockNum:
                inconsistencies = 1
                message = " " + str(my_block_num) + " IN INODE " + fileLineFields[1] + " AT OFFSET " + fileLineFields[3]
                if int(fileLineFields[2]) == 1:
                    print("INVALID INDIRECT BLOCK" + message)
                elif int(fileLineFields[2]) == 2:
                    print("INVALID DOUBLE INDIRECT BLOCK" + message)
                elif int(fileLineFields[2]) == 3:
                    print("INVALID TRIPLE INDIRECT BLOCK" + message)
            elif my_block_num > 0 and my_block_num < firstBlock:
                inconsistencies = 1
                message = " " + str(my_block_num) + " IN INODE " + fileLineFields[1] + " AT OFFSET " + fileLineFields[3]
                if int(fileLineFields[2]) == 1:
                    print("RESERVED INDIRECT BLOCK" + message)
                elif int(fileLineFields[2]) == 2:
                    print("RESERVED DOUBLE INDIRECT BLOCK" + message)
                elif int(fileLineFields[2]) == 3:
                    print("RESERVED TRIPLE INDIRECT BLOCK" + message)
            else:
                if my_block_num > 0:
                    if my_block_num not in block_allocationlist:
                        block_allocationlist[my_block_num] = []
                        block_allocationlist[my_block_num].append((my_block_num, int(fileLineFields[1]), int(fileLineFields[2])+23, int(fileLineFields[3])))
                    else:
                        block_allocationlist[my_block_num].append((my_block_num, int(fileLineFields[1]), int(fileLineFields[2])+23, int(fileLineFields[3])))


def check_datablock():
    for i in range(firstBlock, blockNum):
        if not i in block_allocationlist:
            if not i in block_freelist:
                inconsistencies = 1
                print("UNREFERENCED BLOCK " + str(i))
        elif i in block_allocationlist and i in block_freelist:
            inconsistencies = 1
            print("ALLOCATED BLOCK " + str(i) + " ON FREELIST")
        elif i in block_allocationlist:
            if len(block_allocationlist[i]) > 1:
                inconsistencies = 1
                for saved_block in block_allocationlist[i]:
                    message = " " + str(saved_block[0]) + " IN INODE " + str(saved_block[1]) + " AT OFFSET " + str(saved_block[3])
                    if saved_block[2] >= 12 and saved_block[2] <= 23:
                        print("DUPLICATE BLOCK" + message)
                    elif saved_block[2] == 24:
                        print("DUPLICATE INDIRECT BLOCK" + message)
                    elif saved_block[2] == 25:
                        print("DUPLICATE DOUBLE INDIRECT BLOCK" + message)
                    elif saved_block[2] == 26:
                        print("DUPLICATE TRIPLE INDIRECT BLOCK" + message)

>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8

def checkInode():
    for key in freeList.keys():
        if (key in allocated.keys()):
<<<<<<< HEAD
=======
            inconsistencies = 1
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
            print("ALLOCATED INODE {0} ON FREELIST".format(key))

    for i in range(firstInode, inodeNum + 1):
        if (i not in freeList) and (i not in allocated):
<<<<<<< HEAD
=======
            inconsistencies = 1
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
            print('UNALLOCATED INODE ' + str(i) + ' NOT ON FREELIST')
            unallocatedLinkCount[i] = 1

    for key,value in markedlinkCount.items():
        if(key in realLinkCount.keys()):
            if(realLinkCount[key]==value):
                continue
        else:
<<<<<<< HEAD
            print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, markedlinkCount[key], 0))
            continue
=======
            inconsistencies = 1
            print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, markedlinkCount[key], 0))
            continue
        inconsistencies = 1
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
        print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, markedlinkCount[key], realLinkCount[key]))

    for key, value in unallocatedLinkCount.items():
        if (key in realLinkCount.keys()):
<<<<<<< HEAD
=======
            inconsistencies = 1
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
            print("INODE {0} HAS {1} LINKS BUT LINKCOUNT IS {2}".format(key, 0, realLinkCount[key]))

    for key, value in direntChildInode.items():
        for i in value:
            if i[0] < 1 or i[0] > inodeNum:
<<<<<<< HEAD
                print("DIRECTORY INODE {0} NAME {1} INVALID INODE {2}".format(key, i[1], i[0]))
            elif(i[0] in unallocatedLinkCount.keys()):
=======
                inconsistencies = 1
                print("DIRECTORY INODE {0} NAME {1} INVALID INODE {2}".format(key, i[1], i[0]))
            elif(i[0] in unallocatedLinkCount.keys()):
                inconsistencies = 1
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
                print("DIRECTORY INODE {0} NAME {1} UNALLOCATED INODE {2}".format(key, i[1], i[0]))

            if i[1] == "'..'":
                if int(key) in realParentNode.keys():
                    if realParentNode[int(key)] != i[2]:
<<<<<<< HEAD
=======
                        inconsistencies = 1
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8
                        print("DIRECTORY INODE {0} NAME '..' LINK TO INODE {1} SHOULD BE {2}".format(key, i[2],realParentNode[int(key)]))

            if i[1] == "'.'":
                if int(key) != i[0]:
<<<<<<< HEAD
                    print("DIRECTORY INODE {0} NAME '.' LINK TO INODE {1} SHOULD BE {0}".format(key, i[0]))

=======
                    inconsistencies = 1
                    print("DIRECTORY INODE {0} NAME '.' LINK TO INODE {1} SHOULD BE {0}".format(key, i[0]))
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8

def main():
    if len(sys.argv) != 2:
        print("Invalid Argument")
        sys.exit(1)

    try:
        with open(str(sys.argv[1]), "r") as csv_file:
            read_buf = csv_file.readlines()
            ScanData(read_buf)
            create_blockdic(read_buf)
    except IOError:
        print >>sys.stderr, "Error opening csv file."
        sys.exit(1)

<<<<<<< HEAD
    checkInode()
=======
    check_datablock()
    checkInode()

    if inconsistencies == 1:
        sys.exit(2)
    else:
        sys.exit(0)
>>>>>>> f01bda4ea01811a872ecbe1212cadc76bf0df3a8

if __name__ == "__main__":
    main()
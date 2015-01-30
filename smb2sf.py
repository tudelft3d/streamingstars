#! /usr/bin/python

# smb -> triangle in SimpleFeature

import sys
import struct


#-- setup of the shift for lower-left corner-----------------
#-- put 0 if not shift is wanted
MINX = 0
MINY = 0
#------------------------------------------------------------

def main():
    d = {} #-- dico to store temporarily the vertices/stars
    lastBlock = False
    i = 1
    k = 1
    #-- skip the header of the file
    sys.stdin.read(41)
    while 1:
        element_descriptor = struct.unpack('I', sys.stdin.read(4))[0]
        block = sys.stdin.read(384)
        element_number = len(block) / 12
        if element_number < 32:
            lastBlock = True
        element_counter = 0
        while (element_counter < element_number):
            if (element_descriptor & 1): #-- next element is a vertex
                elem = struct.unpack('fff', block[12*element_counter:12*(element_counter+1)])
                d[i] = (elem[0], elem[1], elem[2])
                i += 1
            else: #-- next element is a face
                elem = struct.unpack('iii', block[12*element_counter:12*(element_counter+1)])
                ids = [elem[0], elem [1], elem[2]]
                for j in range(3):
                    if elem[j] < 0:
                        ids[j] = elem[j] + i
		sys.stdout.write("POLYGON((" + 
		str(MINX + d[ids[0]][0]) + " " +  str(MINY + d[ids[0]][1]) + ", " +
		str(MINX + d[ids[1]][0]) + " " +  str(MINY + d[ids[1]][1]) + ", " + 
		str(MINX + d[ids[2]][0]) + " " +  str(MINY + d[ids[2]][1]) +  ", " +
		str(MINX + d[ids[0]][0]) + " " +  str(MINY + d[ids[0]][1]) + "))\n")
		k += 1
		#-- delete the finalised vertex
                for id in elem: 
                    if id < 0: 
                        del d[i + id]
            element_counter += 1
            element_descriptor = element_descriptor >> 1
        if lastBlock is True:
            break
if __name__ == "__main__":
    main()   
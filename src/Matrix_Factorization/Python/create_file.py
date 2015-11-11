from numpy import *


def create_file(filename2, filename1):
    B = zeros((100000, 3))
    file = open(filename2, "r")
    counter = 0
    while counter < 100000:
        row = file.readline()
        row = row.split("::")
        B[counter] = row[0:3]
        counter += 1
    savetxt(filename1, B, fmt='%.1f', delimiter=",")

from globalvar import *
def board():
    for i in range(0,10,1):
        a[0][i]="#"
        a[9][i]="#"
        a[i][0]="#"
        a[i][9]="#"
    for i in range(1,9,1):
        for j in range(1,9,1):
            a[i][j]=" "



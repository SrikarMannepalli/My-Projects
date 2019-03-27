from globalvar import *
from Spaceship import *
from Aliens import *
class missiles(object):
    def __init__(self,char):
        a[7][Spaceship.position]=char
        os.system('clear')
        for p in range(0,10,1):
            for q in range(0,10,1):
                print(a[p][q],end=' ')
            print()
        print("Score:",missile0.count+missile.count)

class missile(missiles):
    count=0
    time=[-1]
    row=[-1]
    column=[-1]
    def __init__(self):
        missiles.__init__(self,"i")

    def movemissiles(self,i,j,element):
        if a[i-1][j]=="A":
            missile.count+=1
            a[i-1][j]=" "
            a[i][j]=" "
            missile.time.pop(element)
            missile.row.pop(element)
            missile.column.pop(element)
        elif a[i-1][j]=="x":
            a[i-1][j]=" "
            a[i][j]=" "
            missile.time.pop(element)
            missile.row.pop(element)
            missile.column.pop(element)
        elif i==1:
            a[i][j]=" "
            missile.time.pop(element)
            missile.row.pop(element)
            missile.column.pop(element)
        elif a[i-1][j]=="I" or a[i+1][j]=="I":
            a[i][j]=" "
            missile.time.pop(element)
            missile.row.pop(element)
            missile.column.pop(element)
        else:
            a[i-1][j]="i"
            a[i][j]=" "
            missile.time.pop(element)
            missile.row.pop(element)
            missile.column.pop(element)
            missile.time.append(time.time())
            missile.row.append(i-1)
            missile.column.append(j)
        os.system('clear')
        for p in range(0,10,1):
            for q in range(0,10,1):
                print(a[p][q],end=' ')
            print()
        print("Score:",missile0.count+missile.count)

class missile0(missiles):
    count=0
    timer=-200
    time=[-1]
    row=[-1]
    rowfreeze=[-1]
    columnfreeze=[-1]
    column=[-1]
    def __init__(self):
        missiles.__init__(self,"I")

    def move(self,i,j,element):
        if a[i-2][j]=="A":
            missile0.count+=1
            a[i-2][j]="x"
            a[i][j]=" "
            missile0.time.pop(element)
            missile0.row.pop(element)
            missile0.column.pop(element)
            missile0.timer=time.time()
            missile0.rowfreeze.append(i-2)
            missile0.columnfreeze.append(j)
        elif a[i-1][j]=="A":
            missile0.count+=1
            a[i-1][j]="x"
            a[i][j]=" "
            missile0.time.pop(element)
            missile0.row.pop(element)
            missile0.column.pop(element)
            missile0.timer=time.time()
            missile0.rowfreeze.append(i-1)
            missile0.columnfreeze.append(j)
        elif a[i-1][j]=="x":
            a[i-1][j]=" "
            a[i][j]=" "
            missile0.time.pop(element)
            missile0.column.pop(element)
            missile0.row.pop(element)
        elif a[i-2][j]=="x":
            a[i-1][j]=" "
            a[i][j]=" "
            missile0.time.pop(element)
            missile0.column.pop(element)
            missile0.row.pop(element)
        else:
            if i==1 or i==2:
                a[i][j]=" "
                missile0.time.pop(element)
                missile0.row.pop(element)
                missile0.column.pop(element)
            else:
                a[i-2][j]="I"
                a[i][j]=" "
                missile0.time.pop(element)
                missile0.row.pop(element)
                missile0.column.pop(element)
                missile0.time.append(time.time())
                missile0.row.append(i-2)
                missile0.column.append(j)
        os.system('clear')
        for p in range(0,10,1):
            for q in range(0,10,1):
               print(a[p][q],end=' ')
            print()
        print("Score:",missile0.count+missile.count)


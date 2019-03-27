from globalvar import *
class aliens(object):
    row=1
    column=1
    def __init__(self):
        aliens.create(self)

    def create(self):
        global count
        x=random.randrange(1,9,1)
        y=random.randrange(1,3,1)
        while a[y][x]=="x" or a[y][x]=="i" or a[y][x]=="I":
            x=random.randrange(1,9,1)
            y=random.randrange(1,3,1)
        aliens.row=y
        aliens.column=x
        a[y][x]="A"

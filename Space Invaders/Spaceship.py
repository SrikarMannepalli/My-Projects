from globalvar import *
class Spaceship(object):
    position=1
    def __init__(self):
        a[8][1]="^"
        Spaceship.position=1

    def left(self):#moves it to the left if possible
            if Spaceship.position!=1:
                a[8][Spaceship.position]=" "
                Spaceship.position-=1
                a[8][Spaceship.position]="^"

    def right(self):#moves it to the right if possible 
            if Spaceship.position!=8:
                a[8][Spaceship.position]=" "
                Spaceship.position+=1
                a[8][Spaceship.position]="^"


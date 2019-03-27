from Missiles import *
from board import *
board() #creates the board
def printboard():
    os.system('clear')
    for i in range(0,10,1):
        for j in range(0,10,1):
            print(a[i][j],end=' ')
        print()
    print("Score:",missile0.count+missile.count)
printboard()
#function to take the character as input
@timeout_decorator.timeout(0.1, timeout_exception=StopIteration)
def getChar():
        def _ttyRead():
            fd = sys.stdin.fileno()
            oldSettings = termios.tcgetattr(fd)
            try:
                tty.setcbreak(fd)
                answer = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
            return answer
        getChar._func=_ttyRead
        return getChar._func()

class spacecontrol(object):
    def __init__(self):
	    spacecontrol.control(self)

    def control(self):
        bb=time.time()
        aa=time.time()
        cc=time.time()
        space=Spaceship()
        printboard()
        while True:
            try:
                resp=getChar()
            except:
                resp="b"
            if resp=='A':
                os.system('clear')
                space.left()
                printboard()
            elif resp=='D':
                os.system('clear')
                space.right()
                printboard()
            elif resp==' ':
                miss1=missile()
                missile.time.append(time.time())
                missile.row.append(7)
                missile.column.append(Spaceship.position)
                printboard()
            elif resp=='S':
                miss2=missile0()
                missile0.time.append(time.time())
                missile0.row.append(7)
                missile0.column.append(Spaceship.position)
                printboard()
            elif resp=='b':
                pass
            elif resp=='Q':
                os.system('clear')
                sys.exit()
   	
            if time.time()-aa>7.8 and a[aliens.row][aliens.column]!="x":
                a[aliens.row][aliens.column]=" "
            if time.time()-aa>9.8:
                aa=time.time()
                alien=aliens()
                printboard()

            if time.time()-missile0.timer>4.8:
                for l in range(1,len(missile0.rowfreeze),1):
                    if a[missile0.rowfreeze[l]][missile0.columnfreeze[l]]=="x":
                        a[missile0.rowfreeze[l]][missile0.columnfreeze[l]]=" "
                    missile0.rowfreeze.pop()
                    missile0.columnfreeze.pop()

            for missiles in range(1,len(missile.row),1):
                try:
                    if time.time()-missile.time[missiles]>0.9:
                        miss1.movemissiles(missile.row[missiles],missile.column[missiles],missiles)
                except:
                    break

            for missilesnew in range(1,len(missile0.row),1):
                try:
                    if time.time()-missile0.time[missilesnew]>0.9:
                        miss2.move(missile0.row[missilesnew],missile0.column[missilesnew],missilesnew)
                except:
                    break


#calls the spaceship control function
space=spacecontrol()
space()

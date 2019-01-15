# scroll1
# simple example of a scrolling background. This one uses just one picture that
# is drawn to a negative position.
from pygame import *
from math import *
from random import randint



init()
size = width, height = 500, 500
screen = display.set_mode(size)

backPic = image.load("back.jpg")
maskPic = image.load("mask.png")

guyPic = image.load("guy.png")
fnt = font.SysFont("Arial",14)
GREEN = (0,255,0)
def drawScene(screen,guy):
    """ draws the current state of the game """
    offset = 250 - guy[X]
    screen.blit(backPic, (offset,0))
    screen.blit(guyPic, (250,guy[Y]))
        
    display.flip()


def getPixel(mask,x,y):
    if 0<= x < mask.get_width() and 0 <= y < mask.get_height():
        return mask.get_at((int(x),int(y)))[:3]
    else:
        return (-1,-1,-1)

def moveUp(guy,vy):
    for i in range(vy):
        if getPixel(maskPic,guy[X]+15,guy[Y]+2) != GREEN:
            guy[Y] -= 1
        else:
            guy[VY] = 0

def moveDown(guy,vy):
    
    for i in range(vy):
        #print("FALLING",getPixel(backPic,guy[X]+15,guy[Y]+28))
        if getPixel(maskPic,guy[X]+15,guy[Y]+28) != GREEN:
            guy[Y] += 1
        else:
            guy[VY] = 0
            guy[ONGROUND] = True
            
def moveRight(guy,vx):
    for i in range(vx):
        if getPixel(maskPic,guy[X]+28,guy[Y]+15) != GREEN:
            guy[X] += 1

def moveLeft(guy,vx):
    for i in range(vx):
        if getPixel(maskPic,guy[X]+2,guy[Y]+15) != GREEN:
            guy[X] -= 1


'''
climb(guy)
    This 
'''
def climb(guy):
    y = guy[Y] + 27
    while y > guy[Y]+17 and getPixel(maskPic,guy[X],y) == GREEN:
        y-=1
    if y > guy[Y]+17:
        guy[Y] = y - 27
        

'''
    The guy's x position is where he is in the "world" we then draw the map
    at a negative position to compensate.
'''
def moveGuy(guy):
    keys = key.get_pressed()
    guy[ONGROUND] = False
    guy[VY] += 1         # add gravity to VY
    if guy[VY] < 0:
        moveUp(guy,-guy[VY])
    elif guy[VY] > 0:
        moveDown(guy,guy[VY])
        
    if keys[K_LEFT] and guy[X] > 250:
        moveLeft(guy,10)
        climb(guy)
    if keys[K_RIGHT] and guy[X] < 2500:
        moveRight(guy,10)
        climb(guy)
    if keys[K_SPACE] and guy[ONGROUND]:
        guy[VY] = -14
      


running = True         
myClock = time.Clock()

X=0
Y=1
VY=2
ONGROUND=3
SCREENX = 4
guy = [250,50,0,True,250]

while running:
    for evnt in event.get():                # checks all events that happen
        if evnt.type == QUIT:
            running = False

    moveGuy(guy)        

    drawScene(screen, guy)
    myClock.tick(60)
    print (guy[ONGROUND])

quit()

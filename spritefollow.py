"""
sprite3.py
~~~~~~~~~~
This example demonstrates simple sprite animation without using any "fancy" techniques.

"""
from pygame import *

screen = display.set_mode((800,600))

def moveNess():
    global move, frame, NessX, NessY
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_RIGHT]:
        newMove = RIGHT
        NessX += 2
    elif keys[K_DOWN]:
        newMove = DOWN
        NessY += 2
    elif keys[K_UP]:
        newMove = UP
        NessY -= 2
    elif keys[K_LEFT]:
        newMove = LEFT
        NessX -= 2
    else:
        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1

def movePoo():
    global move, frame, PooX, PooY
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_RIGHT]:
        newMove = RIGHT
        PooX += 2
    elif keys[K_DOWN]:
        newMove = DOWN
        PooY += 2
    elif keys[K_UP]:
        newMove = UP
        PooY -= 2
    elif keys[K_LEFT]:
        newMove = LEFT
        PooX -= 2
    else:
        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1
        
def movePaula():
    global move, frame, PaulaX, PaulaY
    keys = key.get_pressed()

    newMove = -1        
    if keys[K_RIGHT]:
        newMove = RIGHT
        PaulaX += 2
    elif keys[K_DOWN]:
        newMove = DOWN
        PaulaY += 2
    elif keys[K_UP]:
        newMove = UP
        PaulaY -= 2
    elif keys[K_LEFT]:
        newMove = LEFT
        PaulaX -= 2
    else:
        frame = 0

    if move == newMove:     # 0 is a standing pose, so we want to skip over it when we are moving
        frame = frame + 0.2 # adding 0.2 allows us to slow down the animation
        if frame >= len(pics[move]):
            frame = 1
    elif newMove != -1:     # a move was selected
        move = newMove      # make that our current move
        frame = 1

def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % ("Ness","Ness",i)))
    return move

def makeMove1(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''

    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % ("Poo","Poo",i)))
    return move

def makeMove2(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % ("Paula","Paula",i)))
    return move






def drawScene():
    screen.fill((255,255,255))
    pic = pics[move][int(frame)]
    pic2 = pics2[move][int(frame)]
    pic3 = pics3[move][int(frame)]
    screen.blit(pic,(NessX-pic.get_width()//2,NessY-pic.get_height()//2))
    screen.blit(pic2,(PooX-pic.get_width()//2,PooY-pic.get_height()//2))
    screen.blit(pic3,(PaulaX-pic.get_width()//2,PaulaY-pic.get_height()//2))
    
    display.flip()




RIGHT = 0 # These are just the indicies of the moves
DOWN = 1  
UP = 2
LEFT = 3

pics = []
pics.append(makeMove("Ness",10,12))      # RIGHT
pics.append(makeMove("Ness",4,6))     # DOWN
pics.append(makeMove("Ness",1,3))    # UP
pics.append(makeMove("Ness",7,9))    # LEFT

pics2 = []
pics2.append(makeMove1("Poo",10,12))      # RIGHT
pics2.append(makeMove1("Poo",4,6))     # DOWN
pics2.append(makeMove1("Poo",1,3))    # UP
pics2.append(makeMove1("Poo",7,9))    # LEFT

pics3 = []
pics3.append(makeMove2("Paula",10,12))      # RIGHT
pics3.append(makeMove2("Paula",4,6))     # DOWN
pics3.append(makeMove2("Paula",1,3))    # UP
pics3.append(makeMove2("Paula",7,9))    # LEFT


frame=0     # current frame within the move
move=2      # current move being performed
NessX, NessY = 400,300
PooX, PooY = 400, 250
PaulaX, PaulaY = 400, 200

running = True
myClock = time.Clock()

while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        
    moveNess()
    movePoo()
    movePaula()
    drawScene()
    myClock.tick(50)
    
quit()

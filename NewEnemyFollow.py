#######################################################################################################
#######################################################################################################
#######################################################################################################
from pygame import *
from random import *
from math import *
from types import ModuleType #From internet, used for some testing

screen = display.set_mode((800,700))
myClock = time.Clock()
maskPic = image.load("Backgrounds and Mask/F1mask.png")
backPic = image.load("Backgrounds and Mask/F1.png")
curmap=[1,0]
role="warrior"

font.init()
init()
font = font.SysFont(None, 20)

GREEN = (0,128,0)
RED =   (255,0,0)
BLACK = (0,0,0)

class Party():#The class for the walking Ness
    def __init__(self,X,Y,direct,idle):
        self.X=X
        self.Y=Y
        self.direct=direct
        self.idle=False
        
    def move(self):
        f = frame//ANIMATION_SPEED % len(picsHero[self.direct])
        pic = picsHero[self.direct][f]
        keys=key.get_pressed()
        if keys[K_RIGHT] and keys[K_DOWN]:
            self.idle=False #Self.idle is whether Ness is idle or not
            self.direct=DOWN
            self.X+=2
            self.Y+=2            
            if maskCollide(self.hitbox(),maskPic):#If the mask is hit, Ness's movement is countered
                self.X-=2
                self.Y-=2
        elif keys[K_LEFT] and keys[K_DOWN]:
            self.idle=False
            self.direct=DOWN
            self.X-=2
            self.Y+=2            
            if maskCollide(self.hitbox(),maskPic):
                self.X+=2
                self.Y-=2
        elif keys[K_RIGHT] and keys[K_UP]:
            self.idle=False
            self.direct=UP
            self.X+=2
            self.Y-=2            
            if maskCollide(self.hitbox(),maskPic):
                self.X-=2
                self.Y+=2
        elif keys[K_LEFT] and keys[K_UP]:
            self.idle=False
            self.direct=UP
            self.X-=2
            self.Y-=2            
            if maskCollide(self.hitbox(),maskPic):
                self.X+=2
                self.Y+=2
        elif keys[K_RIGHT]:
            self.idle=False
            self.direct=RIGHT
            self.X+=3
            if maskCollide(self.hitbox(),maskPic):
                self.X-=3
        elif keys[K_DOWN]:
            self.idle=False
            self.direct=DOWN
            self.Y+=3
            if maskCollide(self.hitbox(),maskPic):
                self.Y-=3
        elif keys[K_UP]:
            self.idle=False
            self.direct=UP
            self.Y-=3
            if maskCollide(self.hitbox(),maskPic):
                self.Y+=3
        elif keys[K_LEFT]:
            self.idle=False
            self.direct=LEFT
            self.X-=3
            if maskCollide(self.hitbox(),maskPic):
                self.X+=3
        else:
            self.idle=True
        #Transitioning between screens
        if self.X+pic.get_width()//2>=795:
            back=mapp[curmap[0]][curmap[1]+1]
            curmap[1]+=1#Curmap is the postition on the map
            update(back[0],back[1])
            self.X=30
        if self.X-pic.get_width()//2<=5:
            back=mapp[curmap[0]][curmap[1]-1]
            curmap[1]+=-1
            update(back[0],back[1])
            self.X=770
        if self.Y+pic.get_height()//2>=695:
            back=mapp[curmap[0]+1][curmap[1]]
            curmap[0]+=1
            update(back[0],back[1])
            self.Y=30
        if self.Y-pic.get_height()//2<=5:
            back=mapp[curmap[0]-1][curmap[1]]
            curmap[0]+=-1
            update(back[0],back[1])
            self.Y=670
            
    def hitbox(self):
        f = frame//ANIMATION_SPEED % len(picsHero[self.direct])
        pic = picsHero[self.direct][f]
        hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        return hitbox
    
    def draw(self):
        f = frame//ANIMATION_SPEED % len(picsHero[self.direct])
        if self.idle==False:
            pic=picsHero[self.direct][f]
        else:
            pic=picsHeroIdle[0][self.direct]
        screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        
class Enemy():#Class for walking enemies
    def __init__(self,direct,moveType,sprite,mask):
        self.direct = direct
        self.moveType = moveType
        self.sprite = sprite
        self.mask=eval(mask)#Each enemy comes with their own mask
        #self.changedirect = {UP:DOWN,DOWN:UP,RIGHT:LEFT,LEFT:RIGHT}
        if self.sprite!="shroom":
            while True:
                self.X=randint(50,750)
                self.Y=randint(50,650)
                if not maskCollide(self.hitbox(),self.mask):
                    break
        else:
            self.X=390
            self.Y=350

    def move(self):
        if self.sprite!="shroom":#Boss doesn't move
            if self.moveType=="Tiny":
                adjust=3
                switchChance=randint(1,5)
            if self.moveType=="Medium":
                adjust=2
                switchChance=randint(1,10)
            if self.moveType=="Fat":
                adjust=1
                switchChance=randint(1,10)
            if self.sprite!="Ghost":#The ghost has different AI that follows you through obstacles
                if switchChance==1:#Changes directions sometimes
                    self.direct=randint(0,3)
                if self.direct==RIGHT:
                    self.X+=adjust
                    if maskCollide(self.hitbox(),self.mask):
                        self.X-=adjust#Counters movement if wall is hit                        
                elif self.direct==DOWN:
                    self.Y+=adjust
                    if maskCollide(self.hitbox(),self.mask):
                        self.Y-=adjust 
                elif self.direct==UP:
                    self.Y-=adjust
                    if maskCollide(self.hitbox(),self.mask):
                        self.Y+=adjust 
                elif self.direct==LEFT:
                    self.X-=adjust
                    if maskCollide(self.hitbox(),self.mask):
                        self.X+=adjust
                        
                if self.X>=780:#Counters movement if the enemies are leaving the screen
                    self.X+=-1
                if self.X<=20:
                    self.X+=1
                if self.Y>=680:
                    self.Y+=-1
                if self.Y<=20:
                    self.X+=1
               
            else:#Spooky Ghosts
                if self.X>part.X:
                    self.X+=choice([0,-1,-2])
                    self.direct=LEFT
                if self.X<part.X:
                    self.X+=choice([0,1,2])
                    self.direct=RIGHT
                if self.Y>part.Y:
                    self.Y+=choice([0,-1,-2])
                    self.direct=UP
                if self.Y<part.Y:
                    self.Y+=choice([0,1,2])
                    self.direct=DOWN
                if self.X>=780:#Counters movement if the enemies are leaving the screen
                    self.X+=-1
                if self.X<=20:
                    self.X+=1
                if self.Y>=680:
                    self.Y+=-1
                if self.Y<=20:
                    self.X+=1
               
       #This all later made the enemies "dance"(spaz), so I came up with a better solution    
    '''def dirSwitch(self): #Albert taught Dictionaries
        #What I had before:
        if self.direct==UP:
            self.direct=DOWN
        if self.direct==DOWN:
            self.direct=UP
        if self.direct==RIGHT:
            self.direct=LEFT
        if self.direct==LEFT:
            self.direct=RIGHT
        self.direct=self.changedirect[self.direct]'''
        
    def hitbox(self):
        if self.sprite=="MadDuck":
            f = frame//ANIMATION_SPEED % len(pics[self.direct])#Some help used here from the exapmle programs
            pic = pics[self.direct][f]
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        if self.sprite=="Chomposaur":
            f = frame//ANIMATION_SPEED % len(pics2[self.direct])
            pic = pics2[self.direct][f]
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        if self.sprite=="Bear":
            f = frame//ANIMATION_SPEED % len(pics3[self.direct])
            pic = pics3[self.direct][f]
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        if self.sprite=="Cultist":
            f = frame//ANIMATION_SPEED % len(pics4[self.direct])
            pic = pics4[self.direct][f]
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        if self.sprite=="Poo":
            f = frame//ANIMATION_SPEED % len(pics5[self.direct])
            pic = pics5[self.direct][f]
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        if self.sprite=="Ghost":
            f = frame//ANIMATION_SPEED % len(pics6[self.direct])
            pic = pics6[self.direct][f]
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        if self.sprite=="shroom":
            pic = pics7[0]#Shroom is special, only has one pic
            hitbox = Rect(self.X-pic.get_width()//2,self.Y-pic.get_height()//2,pic.get_width(),pic.get_height())
        return hitbox
    
    def draw(self):
        if self.sprite=="MadDuck":
            f = frame//ANIMATION_SPEED % len(pics[self.direct])
            pic = pics[self.direct][f]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        if self.sprite=="Chomposaur":
            f = frame//ANIMATION_SPEED % len(pics2[self.direct])
            pic = pics2[self.direct][f]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        if self.sprite=="Bear":
            f = frame//ANIMATION_SPEED % len(pics3[self.direct])
            pic = pics3[self.direct][f]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        if self.sprite=="Cultist":
            f = frame//ANIMATION_SPEED % len(pics4[self.direct])
            pic = pics4[self.direct][f]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        if self.sprite=="Poo":
            f = frame//ANIMATION_SPEED % len(pics5[self.direct])
            pic = pics5[self.direct][f]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        if self.sprite=="Ghost":
            f = frame//ANIMATION_SPEED % len(pics6[self.direct])
            pic = pics6[self.direct][f]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
        if self.sprite=="shroom":
            pic = pics7[0]
            screen.blit(pic,(self.X-pic.get_width()//2,self.Y-pic.get_height()//2))
############
class BattleParty():
  #Class that maintains the stats (health,moves) of the party
    def __init__(self,role):
        if role=="warrior":
            self.movelist=Strip("Stats/WarriorStats.txt")
        if role=="mage":
            self.movelist=Strip("Stats/MageStats.txt")
        if role=="rogue":
            self.movelist=Strip("Stats/RogueStats.txt")
        self.role = self.movelist[0]
        self.curhp = self.movelist[1]
        self.curmp = self.movelist[2]
        self.maxhp = self.movelist[3]
        self.maxmp = self.movelist[4]
        self.abil1 = self.movelist[5]#Ability damage numbers
        self.abil2 = self.movelist[6]
        self.abil3 = self.movelist[7]
        self.abil4 = self.movelist[8]

        self.Move = self.abil1 #current move

    def MoveSelect(self):
  #Function that determines the current move of the player and draws the
  #buttons for the selection
        
        #supposed to be a user prompt but disapears to quickly...
        drawText("What will you do?", font, screen, 10,400, BLACK)
        myClock.tick(300)
        redraw()
        #draws the buttons used in the selection process
        button1.drawButton(button)
        drawMoveText("PUNCH" , font, screen, 300, 499, BLACK)
        button2.drawButton(button)
        drawMoveText("KICK" , font, screen, 500, 499, BLACK)
        button3.drawButton(button)
        drawMoveText("BITE" , font, screen, 300, 566, BLACK)
        button4.drawButton(button)
        drawMoveText("FURY", font, screen, 500, 566, BLACK)
        display.update() 


        #listener for the move selection process. When mouse is clicked
        #the button class checks if click is within button
        picked = 0
        mx,my= mouse.get_pos()
        while picked == 0:
          mx,my = mouse.get_pos()
          for evnt in event.get():
            if evnt.type == QUIT:
              quit()
        
            elif evnt.type == MOUSEBUTTONDOWN:
              if button1.pressed(mx,my) == True:
                self.Move = self.abil1 #assigns the corresponding move
                picked = 1 #conditional to break loop
              if button2.pressed(mx,my) == True:
                self.Move = self.abil2
                picked = 1
              if button3.pressed(mx,my) == True:
                self.Move = self.abil3
                picked = 1 
              if button4.pressed(mx,my) == True:
                self.Move = self.abil4
                picked = 1
        #returns the current move
        return self.Move
        
    def AttackSequence(self,enemy):
      #function that displays a prompt and determunes current health and
      #order 
        screen.blit(background, (0,0))
        displayMessage("You inflicted " + " " +str(self.Move) + "damage!")
        benemy.curhp = Damage(benemy.curhp, self.Move)

class BattleEnemy():
  #Class that maintains the stats (health,moves) of the enemy
    def __init__(self,sprite):
        self.sprite = sprite
        #determines which type the enemy is and makes a list of moves based on it
        if sprite=="MadDuck":
            self.movelist=Strip("Stats/MadDuckStats.txt")
        if sprite=="Chomposaur":
            self.movelist=Strip("Stats/ChomposaurStats.txt")
        if sprite=="Bear":
            self.movelist=Strip("Stats/BearStats.txt")
        if sprite=="Boss":
            self.movelist=Strip("Stats/BossStats.txt")     
        if sprite=="Zombie":
            self.moveList=Strip("Stats/ZombieStats.txt")           
        if sprite=="Cultist":
            self.moveList=Strip("Stats/CultistStats.txt")
        
        self.role = self.movelist[0]   
        self.curhp = self.movelist[1]
        self.curmp = self.movelist[2]
        self.maxhp = self.movelist[3]
        self.maxmp = self.movelist[4]
        self.abil1 = self.movelist[5]#Ability damage numbers
        self.abil2 = self.movelist[6]
        self.abil3 = self.movelist[7]
        self.abil4 = self.movelist[8]

        self.Move = self.abil1 #current move

    def MoveSelect(self):
      #Function that determines selected moves
        self.Move = self.abil1
        return self.Move

    def AttackSequence(self, player):
      #function that displays a prompt and determunes current health and
      #order 
        screen.blit(background, (0,0))
        displayMessage("Enemy inflicted"+ str(self.Move) + "damage!")
        party.curhp = Damage(party.curhp, self.Move)

############
class Button():
  #Class that creates and maintains the buttons
    def assignImage(self, picture):
      #assigns image to button
        self.rect = picture.get_rect()
    def setCoords(self, x,y):
      #assigns coordinates of each button
        self.rect.topleft = x,y
    def drawButton(self, picture):
      #blits and handles the button on screen
        screen.blit(picture, self.rect)
    def pressed(self,mx,my):
      #determines whether or not the mouse click is present
        if self.rect.collidepoint(mx,my)==True:
            return True

class Healthbar():
  #class for creating healthbars for both player and enemy
    def init(self,x,y):
      #Function that initializes the attributes of the health bars
        self.position = x,y
        self.posDimensions = [150,5]
        self.negDimensions = (150,5)
    def drawRects(self):
      #function that draws the rects
        draw.rect(screen, RED,(self.position,self.negDimensions))
        draw.rect(screen, GREEN, (self.position, self.posDimensions))
        display.update()
    def updateBarPlayer(self, PcurrentHp, PmaxHp):
      #function that determines the current length needed for the green.
      #It finds the proportion of remaining health and applies to to the 
      #original (player)
        health = int(PcurrentHp)/int(PmaxHp)
        newBar = health*self.negDimensions[0]
        self.posDimensions[0] = newBar
    def updateBarEnemy(self, EcurrentHp, EmaxHp):
      #function that determines the current length needed for the green.
      #It finds the proportion of remaining health and applies to to the 
      #original (enemy)
        health = int(EcurrentHp)/int(EmaxHp)
        newBar = health*self.negDimensions[0]
        self.posDimensions[0] = newBar
####################
def makeMove(name,start,end):
    ''' This returns a list of pictures. They must be in the folder "name"
        and start with the name "name".
        start, end - The range of picture numbers 
    '''
    move = []
    for i in range(start,end+1):
        move.append(image.load("%s/%s%03d.png" % (name,name,i)))
    return move


def drawScene():#Function used from examples programs
    screen.blit(backPic,(0,0))
    for enemy in enemies:
        enemy.draw()
    part.draw()
    display.flip()


def collide():
    for enemy in enemies:
        if enemy.hitbox().colliderect(part.hitbox()):
            BattleEnemy(enemy.sprite)
            Battle()
            break
            
def maskCollide(box,mask=maskPic):#Looks at four corners and the middle of the right and left sides. Absolute value are not needed
    if mask.get_at((abs(box.x),abs(box.y)))==(255,0,0):
        return True
    if mask.get_at((abs(box.x)+box.width,abs(box.y)+box.height))==(255,0,0):
        return True
    if mask.get_at((abs(box.x),abs(box.y)+box.height))==(255,0,0):
        return True
    if mask.get_at((abs(box.x)+box.width,abs(box.y)))==(255,0,0):
        return True
    if mask.get_at((abs(box.x)+box.width,abs(box.y)+box.height//2))==(255,0,0):
        return True
    if mask.get_at((abs(box.x),abs(box.y)+box.height//2))==(255,0,0):
        return True
    return False

def update(back,enem):#Updates the backgrounds, enemies, and maps after transitioning to a new screen
    global maskPic
    global backPic
    global enemies
    maskPic=image.load("Backgrounds and Mask/"+back+"mask.png")
    backPic=image.load("Backgrounds and Mask/"+back+".png")
    enemies=enem

def moveEnemies(enemies):#This is if multiple baddies are around
        for enemy in enemies:
            enemy.move()
######################
def drawMoveText(text, font, surface, x, y, color):
  #This function forces the text to be drawn from the center of the string

  textobj = font.render(text,1,color)
  textrect = textobj.get_rect()
  textrect.center = (x,y)
  surface.blit(textobj,textrect)
  display.update()

def redraw():
  #this function redraws all the elements of the battle system
  screen.fill((255,255,255))
  screen.blit(background,(0,0))
  
  drawText(party.role, font, screen, 600, 415, BLACK)
  playerBar.updateBarPlayer(party.curhp, party.maxhp)
  playerBar.drawRects()
  drawText(benemy.role, font, screen, 600, 45, BLACK)
  computerBar.updateBarEnemy(benemy.curhp, benemy.maxhp)
  computerBar.drawRects()
  #blits battle image based on the enemy type
  if benemy.sprite=="Bear":
    screen.blit(bear,(70,70))
  if benemy.sprite=="MadDuck":
    screen.blit(duck,(70,70))
  if benemy.sprite=="Boss":
    screen.blit(boss,(70,70))
  if benemy.sprite=="Chomposaur":
    screen.blit(chomposaur,(70,70))
  if benemy.sprite=="Cultist":
    screen.blit(cultist,(70,70))
  if benemy.sprite=="Zombie":
    screen.blit(zombie,(70,70))
    
  display.update()

def drawText(text, font, surface, x, y, color):
#function for simply bliting text on a screen
  if len(text) > 49:
    textLine1 = text[:48]
    textLine2 = text[48:]
  else:
    textLine1 = text
    textLine2 = ""
  
  textobj1 = font.render(textLine1,1,color)
  textrect1 = textobj1.get_rect()
  textrect1.topleft = (x,y)
  surface.blit(textobj1,textrect1)
  display.update()
  
  textobj2 = font.render(textLine2,1,color)
  textrect2 = textobj2.get_rect()
  textrect2.topleft = (x,y+10)
  surface.blit(textobj2,textrect2)
  display.update()

def displayMessage(message):
  #Uses the draw text function to redraw a space and display the statements while in battle
  #kind of useless 
  drawText(message, font, screen, 10,400, BLACK)
  redraw()
  #screen.blit(background, (0,0))

def Strip(file):
  #Function that is responsible for stripping data from a textfile and turning
  #into a list for use when performing moves
    file=open(file).read().strip().split()
    Stats=[]
    Stats.append(file[0])
    
    for i in range(1,9):
        file[i] = int(file[i])
        Stats.append(file[i])

    return Stats

def Damage(hp,Move):
  #function that determines the amount of damage taken per turn
  DMG = int(Move)
  hp = hp - DMG 
  return hp

def world():
  screen.blit(endBack,(0,0))

def Battle():
  #main function that plays out the battle system and ends when either hp is 0
    mixer.music.load("theme2.mp3")
    mixer.music.play()
    winner = ""
    fainted = False
    
    redraw()
    myClock.tick(1000)
    while fainted !=True:
        pMove = party.MoveSelect()
        eMove = benemy.MoveSelect()
        party.AttackSequence(benemy)
        myClock.tick(1000)
        computerBar.updateBarEnemy(benemy.curhp, benemy.maxhp)
        myClock.tick(1000)
        computerBar.drawRects()
        display.update()
        print(int(benemy.curhp))
        if benemy.curhp<0:
            fainted = True
            winner = "player"
            break
            
        benemy.AttackSequence(party)
        myClock.tick(1000)
        computerBar.updateBarPlayer(party.curhp, party.maxhp)
        myClock.tick(1000)
        computerBar.drawRects()
        display.update()
        print(int(party.curhp))
        if party.curhp<0:
            fainted = True
            winner = "enemy"
            break
    '''if winner=="player":
        screen.blit(endBack,(0,0))
    if winner=="enemy":
        screen.blit(endBack(0,0))'''

def collide():
    for enemy in enemies:
        if enemy.hitbox().colliderect(part.hitbox()):
            benemy=BattleEnemy(enemy.sprite)
            party=BattleParty(role)
            Battle()

#######################
RIGHT=0 #Indicies of the directions
DOWN=1  
UP=2
LEFT=3
ANIMATION_SPEED=6


picsHero=[]
picsHero.append(makeMove("Ness",7,8))      # RIGHT
picsHero.append(makeMove("Ness",3,4))     # DOWN
picsHero.append(makeMove("Ness",1,2))    # UP
picsHero.append(makeMove("Ness",5,6))    # LEFT
picsHeroIdle=[]
picsHeroIdle.append(makeMove("Ness",9,12))      # RIGHT
pics=[]
pics.append(makeMove("MadDuck",7,8))      # RIGHT
pics.append(makeMove("MadDuck",3,4))     # DOWN
pics.append(makeMove("MadDuck",1,2))    # UP
pics.append(makeMove("MadDuck",5,6))    # LEFT
pics2=[]
pics2.append(makeMove("Chomposaur",7,8))      # RIGHT
pics2.append(makeMove("Chomposaur",3,4))     # DOWN
pics2.append(makeMove("Chomposaur",1,2))    # UP
pics2.append(makeMove("Chomposaur",5,6))    # LEFT
pics3=[]
pics3.append(makeMove("Bear",7,8))      # RIGHT
pics3.append(makeMove("Bear",3,4))     # DOWN
pics3.append(makeMove("Bear",1,2))    # UP
pics3.append(makeMove("Bear",5,6))    # LEFT
pics4=[]
pics4.append(makeMove("Cultist",7,8))      # RIGHT
pics4.append(makeMove("Cultist",3,4))     # DOWN
pics4.append(makeMove("Cultist",1,2))    # UP
pics4.append(makeMove("Cultist",5,6))    # LEFT
pics5=[]
pics5.append(makeMove("Poo",10,12))      # RIGHT
pics5.append(makeMove("Poo",4,6))     # DOWN
pics5.append(makeMove("Poo",1,3))    # UP
pics5.append(makeMove("Poo",7,9))    # LEFT
pics6=[]
pics6.append(makeMove("Zombie",7,8))      # RIGHT #These are actually ghosts not zombies
pics6.append(makeMove("Zombie",3,4))     # DOWN
pics6.append(makeMove("Zombie",1,2))    # UP
pics6.append(makeMove("Zombie",5,6))    # LEFT
pics7=[image.load("Shrooom.png")]       #Just one pic

frame=0
move=2
running=True
myClock=time.Clock()

#Map names
F1="F1"
F2="F2"
F3="F3"
F4="F4"
F5="F5"
F6="F6"
F9="F9"
XX="ERROR"

#Initalizes the images for the program
background = image.load("Pics/background.png")

endBack = image.load("Pics/gameover.png")
button = image.load("Pics/button.png")  

bear = image.load("Pics/bear1.png")
duck = image.load("Pics/duck1.png")
buffalo = image.load("Pics/buffalo1.png")
chomposaur = image.load("Pics/chomposaur1.png")
croc = image.load("Pics/croc1.png")
dog = image.load("Pics/dog1.png")
cultist = image.load("Pics/cultist1.png")
jack = image.load("Pics/jack1.png")
zombie = image.load("Pics/zombie1.png")
goat = image.load("Pics/goat1.png")
snake = image.load("Pics/snake1.png")
mask1="image.load('Backgrounds and Mask/F1mask.png')"
mask2="image.load('Backgrounds and Mask/F2mask.png')"
mask3="image.load('Backgrounds and Mask/F5mask.png')"
mask4="image.load('Backgrounds and Mask/F9mask.png')"
mask5="image.load('Backgrounds and Mask/F6mask.png')"
mask6="image.load('Backgrounds and Mask/F4mask.png')"

#Making our objects on the map
part=Party(600,175,0,False)
party=BattleParty(role)

E1=[Enemy(randint(0,3),"Tiny","MadDuck",mask1) for i in range(5)]
E2=[Enemy(randint(0,3),"Fat","Chomposaur",mask2) for i in range(2)]
E3=[Enemy(randint(0,3),"Fat","Bear",mask3) for i in range(3)]
E4=[Enemy(randint(0,3),"Tiny","Cultist",mask5) for i in range(3)]
E5=[Enemy(randint(0,3),"Tiny","Ghost",mask4) for i in range(3)]
E6=[Enemy(randint(0,3),"Boss","shroom",mask6)]
enemies=E1
mapp=[
        [[XX,XX],[XX,XX],[F4,E6]],
        [[F1,E1],[XX,XX],[F6,E4]],
        [[F2,E2],[F5,E3],[F9,E5]]]

party = BattleParty("warrior")
benemy = BattleEnemy("Bear")

myClock = time.Clock()

      
running = True

#Initalizes the health bars of the enemy and player
playerBar = Healthbar()
playerBar.init(600,400)
computerBar = Healthbar()
computerBar.init(600,35)

#Initalizes the buttons for the selection process
button1 = Button()
button1.assignImage(button)
button1.setCoords(202, 468)
button2 = Button()
button2.assignImage(button)
button2.setCoords(402, 468)
button3 = Button()
button3.assignImage(button)
button3.setCoords(202, 535)
button4 = Button()
button4.assignImage(button)
button4.setCoords(402, 535)

                
while running:
    for evnt in event.get():
        if evnt.type==QUIT:
            running=False
        
    frame+=1    
    moveEnemies(enemies)
    part.move()
    drawScene()
    collide()
    myClock.tick(30)
    
quit()


#########################################################
#########################################################
#########################################################
#########################################################
################################################################


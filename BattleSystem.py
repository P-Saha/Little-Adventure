from pygame import*
from random import *
from math import*
font.init()
init()
font = font.SysFont(None, 20)

screen = display.set_mode((800,700))

#########################################################

GREEN = (0,128,0)
RED =   (255,0,0)
BLACK = (0,0,0)
#########################################################


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

  

  screen.blit(background, (0,0))

################################################################

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
    

        

    
def Damage(hp,Move):
  #function that determines the amount of damage taken per turn
  DMG = int(Move)
  hp = hp - DMG 
  return hp




#


def world():
  screen.blit(endBack,(0,0))
##############################################################

party = BattleParty("warrior")
benemy = BattleEnemy("Bear")

myClock = time.Clock()


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
        


running = True

#Initalizes the health bars of the enemy and player
playerBar = Healthbar()
playerBar.init(600,400)
computerBar = Healthbar()
computerBar.init(600,35)



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
    
    keys = key.get_pressed()
    if keys[K_RIGHT]:
      Battle() 
    
quit()

        
  

    


    
        

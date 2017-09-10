#defend your ship from the asteroids and enemy saucers
#blowing up enemeny saucers gives you an extra life
#enjoy!
class Ship():#ship class
    def __init__(self):
        
        self.position= PVector(1280/2,720/2)#class level variables
        self.velocity= PVector(0,0)
        self.acceleration= PVector(0,0)
        self.angle=0
        self.angleV=radians(3)
        self.topSpeed=8
        self.timer=0
        
    def update(self):#updates ship position
        global sensitivity
        global keyUp,keyShift,keyLeft,keyRight,shipPos
        self.angleV=radians(sensitivity)
        self.position.add(self.velocity)
        self.velocity.add(self.acceleration)
        self.velocity.limit(self.topSpeed)
        if self.timer>0:#timer for shooting
            self.timer-=1
        if keyRight==True:#key commands
            self.angle+=self.angleV
        if keyLeft==True:
            self.angle-=self.angleV
        if keyUp==True:
            self.acceleration.sub(PVector(cos(self.angle),sin(self.angle)))#calculates acceleration
            self.acceleration.normalize()#normalize acceleration
            self.acceleration.div(4)
        else:
            self.velocity.div(1.005)#makes ship slow down
            self.acceleration=PVector(0,0)
        shipPos=PVector(self.position.x,self.position.y)#send position to a global variable
    
    
    def shoot(self):
        if keyShift==True and self.timer==0:#appends bullets and calculates magnitude and direction
            b.append(PVector(self.position.x,self.position.y))
            bs.append(PVector(cos(self.angle),sin(self.angle)))
            self.timer=10
            
            
    
    def display(self):
        global shipMoveImg,shipImg,keyUp,flicker,flickers,keyDown,sheild, bulletSize
        
        for i in range (0,len(b)):#draw bullets
            noStroke()
            fill(207,254,60)
            ellipse(b[i].x,b[i].y,bulletSize,bulletSize)
            bs[i].normalize()
            bs[i].mult(15)
            b[i].sub(bs[i])
            
            
        for i in range(0,len(b)):#delete bullets
            if b[i].x>1280+bulletSize/2 or b[i].y>720+bulletSize/2 or b[i].x<-bulletSize/2 or b[i].y<-bulletSize/2:
                del(b[i])
                del(bs[i])
                break
        
        pushMatrix()#draw ship
        translate(self.position.x, self.position.y)
        rotate(self.angle)
        if keyUp==True:#makes fire flicker
            flicker+=flickers
            if flicker>2:
                flickers*=-1
            if flicker<1:
                flickers*=-1
            if flicker==1:
                imageMode(CENTER)
                image(shipMoveImg,0,0)
            if flicker!=1:
                imageMode(CENTER)
                image(shipImg,0,0)
        else:
            imageMode(CENTER)
            image(shipImg,0,0)
        popMatrix()
        
        if keyDown==True and sheild>0:#draws sheild
            sheild-=2
            stroke(80,130,250)
            strokeWeight(3)
            fill(80,130,250,30)
            ellipse(self.position.x,self.position.y,90,90)
        if gameStarted==True and gameOver==False:
            stroke(80,130,250)
            strokeWeight(3)
            fill(80,130,250,30)
            rectMode(CENTER)
            rect(width/2,120,sheild,40)
        if keyDown==False and sheild<100:
            sheild+=1
        if sheild>80 and gameStarted==True and gameOver==False:
            fill(255)
            textFont(f,32)
            text("Sheild",width/2,120)
        

    def checkEdges(self):#checks if ship goes off the screen
        if self.position.x>1300:
            self.position.x=-20
        if self.position.x<-20:
            self.position.x=1300
        if self.position.y>730:
            self.position.y=-20
        if self.position.y<-20:
            self.position.y=730

class Roid():#asteroids
    def __init__(self):
    
    
        self.position=[]#class level variables
        self.velocity=[]
        self.create=int(random(0,600))
        self.dir=10
        self.size=[]
        self.die=0
        self.blowUp=[]
        self.blowUpTimer=[]
    def make(self):
        global gameSarted, gameOver
        self.create=int(random(0,600))
        if gameStarted==True and self.create==12 and gameOver==False:#decides when to create asteroids and their direction
            self.size.append(int(random(0,3)))
            self.position.append(PVector(-100,height/2))
            self.dir=int(random(0,4))
            if self.dir==0:
                self.velocity.append(PVector(random(2,4),random(2,4)))
            if self.dir==1:    
                self.velocity.append(PVector(random(2,4),random(-2,-4)))
            if self.dir==2:    
                self.velocity.append(PVector(random(-2,-4),random(2,4)))
            if self.dir==3:    
                self.velocity.append(PVector(random(-2,-4),random(-2,-4)))
        
    
        
    def update(self):
        global score
        for i in range(0,len(self.position)):
            self.position[i].add(self.velocity[i])#moves asteroids
        if gameStarted==True and gameOver==False:
            score+=0.005
        for i in range (0,len(self.blowUp)):#makes explosions appear
            if self.blowUpTimer[i]>0:
                self.blowUpTimer[i]-=1
            if self.blowUpTimer[i]==0:
                del(self.blowUpTimer[i])
                del(self.blowUp[i])
                break
        
    
    def display(self):
        global roid1,roid2,roid3,explosion
        for i in range(0,len(self.position)):
            if self.size[i]==0:
                imageMode(CENTER)
                image(roid1,self.position[i].x,self.position[i].y)#draws asteroids
            if self.size[i]==1:
                imageMode(CENTER)
                image(roid2,self.position[i].x,self.position[i].y)
            if self.size[i]==2:
                imageMode(CENTER)
                image(roid3,self.position[i].x,self.position[i].y)
        for i in range (0,len(self.blowUp)):
            imageMode(CENTER)
            image(explosion,self.blowUp[i].x,self.blowUp[i].y)
    
    def checkEdges(self):# checks if they go off screen
        for i in range(0,len(self.position)):
                if self.position[i].x<-500:
                    del(self.position[i])#deletes stray asteroids
                    del(self.velocity[i])
                    del(self.size[i])
                    break
                break
        for i in range(0,len(self.position)):#wraps them around edges
            if self.position[i].x<-277:
                self.position[i].x=1280+177
            if self.position[i].x>1280+177:
                self.position[i].x=-277
            if self.position[i].y<-277:
                self.position[i].y=720+177
            if self.position[i].y>720+177:
                self.position[i].y=-277
            
    
    def collides(self):
         global shipPos, score, bulletSize
         for i in range (0,len(self.position)):
            for k in range(0,len(b)):#bullet/asteroid collisions
                if self.size[i]==0 and dist(b[k].x,b[k].y,self.position[i].x,self.position[i].y)<(177/2+bulletSize/2):
                    self.blowUp.append(PVector(self.position[i].x,self.position[i].y))#what happens when they collide
                    self.blowUpTimer.append(10)
                    self.size[i]=1
                    self.velocity[i].mult(-1)
                    b[k]=PVector(-1000,-1000)
                    self.position.append(PVector(self.position[i].x,self.position[i].y))
                    self.velocity.append(PVector((self.velocity[i].x)*(-1),(self.velocity[i].y)*(-1)))
                    self.size.append(1)
                    score+=177
                if self.size[i]==1 and dist(b[k].x,b[k].y,self.position[i].x,self.position[i].y)<(123/2+bulletSize/2):
                    self.blowUp.append(PVector(self.position[i].x,self.position[i].y))
                    self.blowUpTimer.append(10)
                    self.size[i]=2
                    self.velocity[i].mult(-1)
                    b[k]=PVector(-1000,-1000)
                    self.position.append(PVector(self.position[i].x,self.position[i].y))
                    self.velocity.append(PVector((self.velocity[i].x)*(-1),(self.velocity[i].y)*(-1)))
                    self.size.append(2)
                    score+=123
                if self.size[i]==2 and dist(b[k].x,b[k].y,self.position[i].x,self.position[i].y)<(64/2+bulletSize/2):
                    self.blowUp.append(PVector(self.position[i].x,self.position[i].y))
                    self.blowUpTimer.append(10)
                    self.position[i]=PVector(-1000,-1000)
                    b[k]=PVector(-1000,-1000)
                    score+=64
                    
    def hitShip(self):
         global shipPos, lives, gameOver,sheild
         print(sheild)
         if keyDown==False or sheild<=2:
            for i in range (0,len(self.position)):#ship/asteroid collisions
                if self.size[i]==0 and dist(shipPos.x,shipPos.y,self.position[i].x,self.position[i].y)<(104.5):
                    self.position[i]=PVector(-1000,-1000)
                    lives-=1
                    self.die=5
                if self.size[i]==1 and dist(shipPos.x,shipPos.y,self.position[i].x,self.position[i].y)<(77.5):
                    self.position[i]=PVector(-1000,-1000)
                    lives-=1
                    self.die=5
                if self.size[i]==2 and dist(shipPos.x,shipPos.y,self.position[i].x,self.position[i].y)<(48):
                    self.position[i]=PVector(-1000,-1000)
                    lives-=1
                    self.die=5
            for i in range(0,len(sb)):#enemy bullet/ship collisions
                if dist(sb[i].x,sb[i].y,shipPos.x,shipPos.y)<18:
                    sb[i]=PVector(1000,1000)
                    lives-=1
                    self.die=5
         if self.die>0:#hit screen
            image(bars,bars.width/2,bars.height/2)
            self.die-=1
            
         if lives<1:#what happens when you loose all lives
            
            gameOver=True
            image(endScreen,endScreen.width/2,endScreen.height/2)
            bs=[]
            sbs=[]
            sheild=100
            self.position=[]
            self.velocity=[]
            self.size=[]
            
    
class Saucer():#enemey ship
    def __init__(self):
        self.position=[]
        self.velocity=[]
        self.create=random(0,1000)
        self.timer=0
        self.blowUp=[]
        self.blowUpTimer=[]
    
    def make(self):
        global gameSarted, gameOver
        self.create=int(random(0,1000))#creates ship (in almost the exact same way as the asteroids)
        if gameStarted==True and self.create==12 and gameOver==False:
            self.position.append(PVector(-100,random(100,620)))
            self.velocity.append(PVector(random(2,5),random(-1,1)))
    def update(self):
        global gameStarted, gameOver, score
    
        for i in range(0,len(self.position)):
            self.position[i].add(self.velocity[i])#deletes of screen ships
            if self.position[i].x>1400:
                del(self.position[i])
                del(self.velocity[i])
                break
        for i in range (0,len(sb)):#draws and calculates saucer bullets
            noStroke()
            fill(207,254,60)
            ellipse(sb[i].x,sb[i].y,4,4)
            sbs[i].normalize()
            sbs[i].mult(7)
            sb[i].add(sbs[i])
        for i in range(0,len(sb)):#delete off screen saucer bullets
            if sb[i].x>1282 or sb[i].y>722 or sb[i].x<-2 or sb[i].y<-2:
                del(sb[i])
                del(sbs[i])
                break
        if self.timer>0:#shooting timer
            self.timer-=1
        for i in range (0,len(self.blowUp)):#saucers explode
            if self.blowUpTimer[i]>0:
                self.blowUpTimer[i]-=1
            if self.blowUpTimer[i]==0:
                del(self.blowUpTimer[i])
                del(self.blowUp[i])
                break
        if keyPressed and keyCode==CONTROL and gameStarted==True and gameOver==False:#press control to append ships
            self.position.append(PVector(-100,random(100,620)))
            self.velocity.append(PVector(random(2,5),random(-1,1)))
            score-=9999
            
    def display(self):
        for i in range(0,len(self.position)):#draws ships and explosions
            imageMode(CENTER)
            image(saucerImg,self.position[i].x,self.position[i].y)
        for i in range (0,len(self.blowUp)):
            imageMode(CENTER)
            image(explosion,self.blowUp[i].x,self.blowUp[i].y)
        
    def shoot(self):#makes the enemy ship shoot towards you 
        global ShipPos
        if self.timer==0 and gameOver==False:
            for i in range(0,len(self.position)):
            
                sb.append(PVector(self.position[i].x,self.position[i].y))
                sbs.append(PVector(shipPos.x-self.position[i].x,shipPos.y-self.position[i].y))
                
            self.timer=80
        
    def hit(self):
        global score,lives,bulletSize
        for i in range(0,len(self.position)):
            for k in range(0,len(b)):#collisions saucer/bullets
                if gameOver==False:
                    if dist(self.position[i].x,self.position[i].y-10,b[k].x,b[k].y)<30+bulletSize/2 or dist(self.position[i].x-30,self.position[i].y,b[k].x,b[k].y)<15+bulletSize/2 or dist(self.position[i].x+30,self.position[i].y,b[k].x,b[k].y)<15+bulletSize/2:
                        self.blowUp.append(PVector(self.position[i].x,self.position[i].y))
                        self.blowUpTimer.append(10)
                        b[k]=PVector(1000,1000)
                        self.position[i]=PVector(1000,1000)
                        score+=200
                        lives+=1

class Power():#powerUps
    def __init__(self):
        self.position=[]
        self.velocity=[]
        self.create=random(0,3000)
    
        
    
    def make(self):
        global gameSarted, gameOver
        self.create=int(random(0,3000))#makes powerups much like saucer and roids
        if gameStarted==True and self.create==12 and gameOver==False:
            self.position.append(PVector(-100,random(100,620)))
            self.velocity.append(PVector(random(2,5),random(-1,1)))
    def update(self):
        global gameStarted, gameOver, score
    
        for i in range(0,len(self.position)):#delete off screen powerups
            self.position[i].add(self.velocity[i])
            if self.position[i].x>1400:
                del(self.position[i])
                del(self.velocity[i])
                break
    
    
    
        if keyPressed and keyCode==49 and gameStarted==True and gameOver==False:#press 1 to append power ups
            self.position.append(PVector(-100,random(100,620)))
            self.velocity.append(PVector(random(2,5),random(-1,1)))
            score-=9999
            
    def display(self):#draws powerUps
        for i in range(0,len(self.position)):
            imageMode(CENTER)
            image(powerUpImg,self.position[i].x,self.position[i].y)
    
        
    
        
    def hit(self):
        global score,lives,bulletSize,sheild
        for i in range(0,len(self.position)):#power up/bullet collisions and what powerup does 
            for k in range(0,len(b)):
                if gameOver==False:
                    if dist(self.position[i].x,self.position[i].y,b[k].x,b[k].y)<50+bulletSize/2:
                    
                        b[k]=PVector(1000,1000)
                        self.position[i]=PVector(1000,1000)
                        sheild+=100
                        bulletSize=30
        if sheild<=100:
            bulletSize=4
        
                            
            
    
ship=Ship()#global variables
roid=Roid()
saucer=Saucer()
power=Power()
gameStarted=False
flicker=0
flickers=1
startX=0
b=[]#bullets
bs=[]#bullet speed
bulletSize=4
sb=[]#saucer bullet
sbs=[]#saucer bullet speed
shipPos=PVector(1280/2,720/2)
lives=3
score=0
gameOver=False
howTo=False
sensitivity=3
sliderX=160
sheild=100



def setup():

    global startScreen,back,shipImg,shipMoveImg,roid1,roid2,roid3,f,endScreen,bars,how,explosion,f2,saucerImg,powerUpImg
    size(1280,720)
    startScreen=loadImage("start.jpg")#load images /fonts
    back=loadImage("background.JPG")
    shipImg=loadImage("ship.png")
    shipMoveImg=loadImage("ship2.png")
    roid1=loadImage("roid1.png")
    roid2=loadImage("roid2.png")
    roid3=loadImage("roid3.png")
    endScreen=loadImage("end.jpg")
    bars=loadImage("bars.png")
    how=loadImage("how.jpg")
    explosion=loadImage("explosion.png")
    f=loadFont("Trench-Thin-100.vlw")
    f2=loadFont("Trench-Thin-30.vlw")
    saucerImg=loadImage("saucer.png")
    powerUpImg=loadImage("powerUP.png")

    


def draw():
    global ship,gameStarted,startX,roid,saucer,score,lives,gameOver,howTo,sliderX,sensitivity,power
    imageMode(CORNER)
    image(back,0,0)
    if gameStarted==False and mousePressed:#start screen dissapears when you click
        gameStarted=True
    if gameStarted==True and startX<width+1:
        startX+=100

#177,177 big roid
#123,123 medium roid
#64,64 small roid

    if startX<width:
        imageMode(CORNER)
        image(startScreen,startX,0)
    if howTo==True and gameStarted==False:#how to screen with sensitivity slider
        imageMode(CENTER)
        image(how,how.width/2,how.height/2)
        noStroke()
        fill(255)
        rect(100,160,400,60,20)
        fill(0)
        rect(sliderX,160,60,60,20)
        if mouseX>130 and mouseX<470 and mouseY>150 and mouseY<230:
            sliderX=mouseX-30
        textFont(f,32)
        text("Sensitivity: "+str(int(((sliderX-84)/400.0)*100)+12)+"%",120,140)
        sensitivity=int(((((sliderX-84)/400.0)*100)+12)/6.67)
    ship.shoot()
    ship.update()#call classes
    ship.display()
    ship.checkEdges()
    roid.update()
    roid.make()
    roid.display()
    roid.checkEdges()
    roid.collides()
    roid.hitShip()
    saucer.make()
    saucer.shoot()
    saucer.update()
    saucer.display()
    saucer.hit()
    power.make()
    power.update()
    power.display()
    power.hit()
    
    
    if gameStarted==True and gameOver==False:#prints game display
        textAlign(CENTER,CENTER)
        textFont(f,48)
        fill(255)
        text("Lives: "+str(lives)+"   Score: "+str(int(score)),width/2,75)
        textFont(f2,18)
        text("©Tom Ginsberg, 2015®",width/2,680)
    list=split(str(int(score)), ' ')#saves top score in file
    loadScore=loadStrings("bestScore.txt")
    bestScore=int(loadScore[0])
    currentScore=int(list[0])
    if currentScore>bestScore:
        saveStrings("bestScore.txt", list)
    if gameOver==True:#prints score at the end of the game
        fill(0)
        textFont(f,40)
        text("Best score:"+" "+str(int(bestScore)),1000,300)
        text("Best score:"+" "+str(int(bestScore)),1001,301)
    
        text("Your score:"+" "+str(int(score)),650,300)
        text("Your score:"+" "+str(int(score)),651,301)    
    
    if gameOver==True and mousePressed:#restarts game
        gameOver=False
        lives=3
        score=0
        gameStarted=False
        startX=0
    if gameStarted==False and keyPressed and keyCode==67:#get howto screen
        howTo=True
    if gameStarted==False and keyPressed and keyCode==66:#goes back
        howTo=False
    
    
        

    
    
keyUp = False#key variables
keyRight = False
keyLeft = False
keyShift = False
keyDown = False
    
def keyPressed():
    global keyUp,keyShift,keyLeft,keyRight,keyDown#checks if key is pressed
    if key == CODED:
        if (keyCode == UP):
            keyUp = True
        if (keyCode == SHIFT):
            keyShift = True
        if (keyCode == LEFT):
            keyLeft = True
        if (keyCode == RIGHT):
            keyRight = True
        if (keyCode == DOWN):
            keyDown = True


def keyReleased():
    global keyUp,keyShift,keyLeft,keyRight,keyDown#checks if key is released
    if (key == CODED):
        if (keyCode == UP):
            keyUp = False
        if (keyCode == SHIFT):
            keyShift = False
        if (keyCode == LEFT):
            keyLeft = False
        if (keyCode == RIGHT):
            keyRight = False
        if (keyCode == DOWN):
            keyDown = False
    
def mousePressed():
    if mousePressed and gameStarted==True and gameOver==False:#click to pause
        noLoop()
def mouseReleased():
    loop()
    


import pygame, sys, time, random

pygame.init()




        

#Resources
#Clocks to tick(count)
clock = pygame.time.Clock()
#Screen Display
window_width = 1920/2
window_height = 1080/2
screen = pygame.display.set_mode((window_width, window_height),pygame.RESIZABLE)
background = pygame.image.load("resources/background/bg_img.jpeg")
background = pygame.transform.scale(background, (window_width, window_height))
font = pygame.font.SysFont("helvetica", 30, 1, 1)
pygame.display.set_caption("Displaying Text")

#Soldier Walk Frames
walkRight = [pygame.image.load(f'resources/sprite/soldier/R{i}.png') for i in range (1, 10)]
walkLeft = [pygame.image.load(f'resources/sprite/soldier/L{i}.png') for i in range (1, 10)]
charStill = pygame.image.load('resources/sprite/soldier/standing.png')

#Enemy Walk Frames
enemyRight = [pygame.image.load(f'resources/sprite/enemy/R{i}.png') for i in range (1, 10)]
enemyLeft = [pygame.image.load(f'resources/sprite/enemy/L{i}.png') for i in range (1, 10)]



#Classes

#Player Class
class Player():
    def __init__(self, xpos, ypos, objectwidth, objectheight):
        #Creating moving object
        #Position
        self.xpos = xpos
        self.ypos = ypos
        #Size
        self.objectwidth = objectwidth
        self.objectheight = objectheight
        #Directional
        self.isLeft = False
        self.isRight = False
        self.vel = 5
        self.walkCnt = 0
        self.standing = True

        #Currently has no use, but hitbox for player
        self.hitbox = (self.xpos, self.ypos, self.objectwidth, self.objectheight)
        self.hit = pygame.Rect(self.hitbox)

    def draw(self, screen):
        #Tick for animations
        if self.walkCnt + 1 >= 18:
            self.walkCnt = 0
        
        #Soldier Animations
        if not self.standing:
            if self.isLeft:
                screen.blit(walkLeft[self.walkCnt//2], (self.xpos, self.ypos))
                self.walkCnt += 1
            elif self.isRight:
                screen.blit(walkRight[self.walkCnt//2], (self.xpos, self.ypos))
                self.walkCnt += 1
        else:
            if self.isRight:
                screen.blit(walkRight[0], (self.xpos, self.ypos))
            else:
                screen.blit(walkLeft[0], (self.xpos, self.ypos))
        #Drawing and updating hitboxes
        self.hitbox = (self.xpos, self.ypos, self.objectwidth, self.objectheight)
        self.hit = pygame.Rect(self.hitbox)

#Projectile Class
class Projectile():
    def __init__(self, xpos, ypos, radius, color, direction):
        #Creating moving object
        #Position
        self.xpos = xpos
        self.ypos = ypos
        #Size
        self.radius = radius
        self.color = color
        #Direction
        self.direction = direction
        self.vel = 8 * direction
        #Hitbox
        self.hit = pygame.Rect(self.xpos, self.ypos, self.radius, self.radius)

    
    def draw(self, screen):
        #Drawing bullet and updating hitbox
        pygame.draw.circle(screen, self.color, (self.xpos, self.ypos), self.radius)
        self.hit = pygame.Rect(self.xpos, self.ypos, self.radius, self.radius)
        
#Enemy Class
class Enemy():



    def __init__(self, xpos, ypos, objectheight, objectwidth, end):
        #Creating moving object
        #Position
        self.xpos = xpos
        self.ypos = ypos
        self.path = [xpos, end]
        #Size
        self.objectwidth = objectwidth
        self.objectheight = objectheight
        #Directional
        self.isLeft = False
        self.isRight = False
        self.vel = 1
        self.walkCnt = 0

        #Hitbox
        self.hitbox = (self.xpos + 20, self.ypos + 15, self.objectwidth - 40, self.objectheight - 15)
        self.hit = pygame.Rect(self.hitbox)
    
    def draw(self, screen):
        self.movement()
        #Tick for animations
        if self.walkCnt + 1 >= 18:
            self.walkCnt = 0
        
        #Enemy Animations
        if self.vel > 0:
            screen.blit(enemyRight[self.walkCnt//2], (self.xpos, self.ypos))
            self.walkCnt += 1
        else:
            screen.blit(enemyLeft[self.walkCnt//2], (self.xpos, self.ypos))
            self.walkCnt += 1
        #Updating hit box and hitting.
        self.hitbox = (self.xpos + 20, self.ypos + 15, self.objectwidth - 40, self.objectheight - 15)
        self.hit = pygame.Rect(self.hitbox)

    def movement(self):
        #Continually moves enemy
        if self.xpos < self.path[1]:
            self.xpos += self.vel




#Errors
#Use tick to stall bullets instead of using the counter on line 201. This will stop it from sometimes not 
#being able to shoot.
#



def main():
    global keepHealth, soldierHealth, score, enemies, enemy, bullet, bullets, soldier, clock, window_height, window_width, background, screen
    
    #Init Player
    soldier = Player(415, 395, 64, 64)
    
    #Enemy spawning holders and data
    lanes = [415, 385, 355]
    enemies = []
    enemiesDefeated = 0
    
    #Bullet holders and data
    bullets = []
    bulletTimerStart = 0
    bulletTimer = -1

    #Start Tick for Score
    startTick = time.time()

    #Healths
    soldierHealth = 100
    keepHealth = 100

    #Game Loop
    drop = False
    while not drop:

        #Checks for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop = True

        #Score
        score = ((time.time() - startTick)//.01) + (enemiesDefeated * 100)
        print(score)

        #Enemy Spawn data
        randomLane = random.randint(0,2)
        #Little Soldier Spawn Iterator
        enemySoldierIteration = (score//2500) + 1


        #Enemy Holder
        for enemy in enemies:
            if enemy.xpos < window_width and enemy.xpos > -50:
                enemy.xpos += enemy.vel
            elif enemy.xpos > window_width:
                keepHealth -= 10
                enemies.pop(enemies.index(enemy))
        #Enemy Spawning
        #This causes issues where the enemy cannot detect the collision FIXED by using double for loop in bullet loop
        if len(enemies) < enemySoldierIteration:
            enemies.append(Enemy(-50, lanes[randomLane], 64, 64, (window_width + 10)))
    
        #Bullet Timer
        differentialScoreLogic = 3 - score/12500
        if differentialScoreLogic <= 0.75:
            differentialScoreLogic = 0.75
        if bulletTimerStart != 0:
            bulletTimer = time.time() - bulletTimerStart
            if bulletTimer >= differentialScoreLogic:
                bulletTimer = -1
                bulletTimerStart = 0

        
        #Bullet Holder
        for bullet in bullets:
            #Add for loop to iterator through enemies as well
            for enemy in enemies:
            #Hitbox collision
                if bullet.hit.colliderect(enemy.hit):
                    bullets.pop(bullets.index(bullet))    
                    enemies.pop(enemies.index(enemy))
            #Moves bullet if it has not gone off screen
            if bullet.xpos < window_width and bullet.xpos > 0:
                bullet.xpos += bullet.vel
            #Deletes bullet if it moves off screen
            else:
                bullets.pop(bullets.index(bullet))

        #Key inputs
        KEY = pygame.key.get_pressed()

        #Shoots bullets
        if (KEY[pygame.K_x]) and bulletTimer == -1:
            bulletTimerStart = time.time()
            if soldier.isRight:
                direction = 1
            else:
                direction = -1

            if len(bullets) < 5:
                bullets.append(Projectile((soldier.xpos + soldier.objectwidth//2), (soldier.ypos + soldier.objectheight//2), 6, "black", direction))
        #Move up
        if (KEY[pygame.K_UP] or KEY[pygame.K_w]) and soldier.ypos > 345:
            soldier.ypos -= soldier.vel
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.ypos -= 3
        #Move down
        elif (KEY[pygame.K_DOWN] or KEY[pygame.K_s]) and soldier.ypos < 445:
            soldier.ypos += soldier.vel
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.ypos += 3
        #Move left
        if (KEY[pygame.K_LEFT] or KEY[pygame.K_a]) and soldier.xpos > 50:
            soldier.xpos -= soldier.vel
            soldier.isLeft = True
            soldier.isRight = False
            soldier.standing = False
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.xpos -= 3
        #Move right
        elif (KEY[pygame.K_RIGHT] or KEY[pygame.K_d]) and soldier.xpos < window_width - soldier.objectwidth:
            soldier.xpos += soldier.vel
            soldier.isLeft = False
            soldier.isRight = True
            soldier.standing = False
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.xpos += 3
        
        #Checks if Player is standing and faces him the last direction
        else:
            soldier.standing = True
            soldier.walkCnt = 0

        
        #Wipes old objects/characters & draws in new
        DrawIn()


#Draws Everything in Game Loop
def DrawIn():
    
    #Draws background
    screen.blit(background, (0, 0)) 
    drawScore = font.render("Score: " + str(score), 0, "black")
    screen.blit(drawScore, (window_width/2 - 150, 10))
    drawKeepHealth = font.render("Keep Health: " + str(keepHealth), 0, "black")
    screen.blit(drawKeepHealth, (window_width/2 - 150, 40))
    #Drawing moving objects
    #Draws in multiple enemies
    for enemy in enemies:
        enemy.draw(screen)
    #Draw in tanks

    #Draw in grenades

    #Draws in multiple bullets
    for bullet in bullets:
        bullet.draw(screen)
    soldier.draw(screen)

    #Frame Rate
    clock.tick(30)
    #Updates screen continually
    pygame.display.flip()

#Runs main function of code
main()
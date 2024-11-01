import pygame, sys, time, random

pygame.init()




        

#Resources
# Clocks
clock = pygame.time.Clock()
#Screen Display
window_width = 1920/2
window_height = 1080/2
screen = pygame.display.set_mode((window_width, window_height),pygame.RESIZABLE)
background = pygame.image.load("resources/background/bg_img.jpeg")
background = pygame.transform.scale(background, (window_width, window_height))
pygame.display.set_caption("Character Animation")

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

    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.xpos, self.ypos), self.radius)
        


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

    def movement(self):
        if self.xpos < self.path[1]:
            self.xpos += self.vel

        





#Enemy Arrays

def main():
    global enemies, enemy, bullets, soldier, clock, window_height, window_width, background, screen, xpos, ypos, isLeft, isRight, vel, walkCnt
    

    soldier = Player(415, 395, 64, 64)
    
    lanes = [415, 385, 355]
    enemies = []
    enemiesDefeated = 0
    #enemy = Enemy(-5, 415, 64, 64, window_width)
    bullets = []
    bulletWait = 0
    startTick = time.time()
    #Game Loop
    drop = False
    while not drop:
        #Score
        score = ((time.time() - startTick)//.01) + (enemiesDefeated * 100)
        print(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop = True
    
        #Bullet Wait
        if bulletWait < 3:
            bulletWait += 1
            if bulletWait == 3:
                bulletWait = 0

        
        #Bullet Holder
        for bullet in bullets:
            if bullet.xpos < window_width and bullet.xpos > 0:
                bullet.xpos += bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        #Enemy Holder
        for enemy in enemies:
            if enemy.xpos < window_width and enemy.xpos > -50:
                enemy.xpos += enemy.vel
            else:
                enemies.pop(enemies.index(enemy))
        #Enemy Spawning
        randomLane = random.randint(0,2)
        i = (score//250) + 1
        
        if len(enemies) < i:
            enemies.append(Enemy(-50, lanes[randomLane], 64, 64, (window_width + 10)))

        #Key inputs
        KEY = pygame.key.get_pressed()
        if (KEY[pygame.K_x]) and bulletWait == 0:
            if soldier.isRight:
                direction = 1
            else:
                direction = -1

            if len(bullets) < 3:
                bullets.append(Projectile((soldier.xpos + soldier.objectwidth//2), (soldier.ypos + soldier.objectheight//2), 6, "black", direction))
        if (KEY[pygame.K_UP] or KEY[pygame.K_w]) and soldier.ypos > 345:
            soldier.ypos -= soldier.vel
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.ypos -= 3
        elif (KEY[pygame.K_DOWN] or KEY[pygame.K_s]) and soldier.ypos < 445:
            soldier.ypos += soldier.vel
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.ypos += 3
        if (KEY[pygame.K_LEFT] or KEY[pygame.K_a]) and soldier.xpos > 50:
            soldier.xpos -= soldier.vel
            soldier.isLeft = True
            soldier.isRight = False
            soldier.standing = False
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.xpos -= 3
        elif (KEY[pygame.K_RIGHT] or KEY[pygame.K_d]) and soldier.xpos < window_width - soldier.objectwidth:
            soldier.xpos += soldier.vel
            soldier.isLeft = False
            soldier.isRight = True
            soldier.standing = False
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                soldier.xpos += 3
        

        else:
            soldier.standing = True
            soldier.walkCnt = 0

        
        #Wipes old objects/characters
        DrawIn()


#Draws Everything in Game Loop
def DrawIn():
    screen.blit(background, (0, 0)) #Draws background
    
    for enemy in enemies:
        enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    soldier.draw(screen)

    #Frame Rate
    clock.tick(30)
    #Updates screen continually
    pygame.display.flip()




main()
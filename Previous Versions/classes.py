import pygame
import sys
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
        print(self.standing)
        #Soldier Animations
        if not(self.standing):
            if self.isLeft:
                screen.blit(walkLeft[self.walkCnt//2], (self.xpos, self.ypos))
                self.walkCnt += 1
                #print("Animation Frame:" + self.walkCnt)
            elif self.isRight:
                screen.blit(walkRight[self.walkCnt//2], (self.xpos, self.ypos))
                self.walkCnt += 1
                #print("Animation Frame:" + self.walkCnt)
        else:
            if self.isRight:
                screen.blit(walkRight[0], (self.xpos, self.ypos))
                #print("Error Test")
            else:
                screen.blit(walkLeft[0], (self.xpos, self.ypos))
                #print("Error Test")


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
        


def main():
    global bullets, soldier, clock, window_height, window_width, background, screen
    

    soldier = Player(415, 395, 64, 64)
    bullets = []
    bulletWait = 0
    #Game Loop
    drop = False
    while not drop:
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

        #Key inputs
        KEY = pygame.key.get_pressed()

        if (KEY[pygame.K_SPACE]) and bulletWait == 0:
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
        elif (KEY[pygame.K_LEFT] or KEY[pygame.K_a]) and soldier.xpos > 50:
            soldier.xpos -= soldier.vel
            soldier.isLeft = True
            soldier.isRight = False
            soldier.standing = False
            print(soldier.isLeft)
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

        
        #Wipes old objects/characters
        DrawIn()


#Draws Everything in Game Loop
def DrawIn():
    screen.blit(background, (0, 0)) #Draws background
    soldier.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    #Frame Rate
    clock.tick(30)
    #Updates screen continually
    pygame.display.flip()




main()
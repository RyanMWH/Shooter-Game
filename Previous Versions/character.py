import pygame
import sys
pygame.init()

#Global Variables


        

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
    
#Creating moving object
#Position
xpos = 415
ypos = 395
#Size
objectwidth = 50
objectheight = 50
#Directional
isLeft = False
isRight = False
vel = 5
walkCnt = 0

#Soldier
walkRight = [pygame.image.load(f'resources/sprite/soldier/R{i}.png') for i in range (1, 10)]
walkLeft = [pygame.image.load(f'resources/sprite/soldier/L{i}.png') for i in range (1, 10)]
charStill = pygame.image.load('resources/sprite/soldier/standing.png')
#Enemy Arrays

def main():
    global clock, window_height, window_width, background, screen, xpos, ypos, isLeft, isRight, vel, walkCnt
    #Game Loop
    drop = True
    while drop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                drop = False


        #Key inputs
        KEY = pygame.key.get_pressed()
        if (KEY[pygame.K_UP] or KEY[pygame.K_w]) and ypos > 345:
            ypos -= vel
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                ypos -= 3
        if (KEY[pygame.K_DOWN] or KEY[pygame.K_s]) and ypos < 445:
            ypos += vel
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                ypos += 3
        if (KEY[pygame.K_LEFT] or KEY[pygame.K_a]) and xpos > 50:
            xpos -= vel
            isLeft = True
            isRight = False
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                xpos -= 3
        elif (KEY[pygame.K_RIGHT] or KEY[pygame.K_d]) and xpos < window_width - objectwidth:
            xpos += vel
            isLeft = False
            isRight = True
            if KEY[pygame.K_LSHIFT] or KEY[pygame.K_RSHIFT]:
                xpos += 3
        else:
            isLeft = False
            isRight = False
            walkCnt = 0

        
        #Wipes old objects/characters
        DrawIn()


#Draws Everything in Game Loop
def DrawIn():
    global walkCnt
    screen.blit(background, (0, 0)) #Draws background
    
    #Frame Rate
    clock.tick(30)
    #Tick for animations
    if walkCnt + 1 >= 18:
        walkCnt = 0
    
    #Soldier Animations
    if isLeft:
        screen.blit(walkLeft[walkCnt//2], (xpos, ypos))
        walkCnt += 1
    elif isRight:
        screen.blit(walkRight[walkCnt//2], (xpos, ypos))
        walkCnt += 1
    else:
        screen.blit(charStill, (xpos, ypos))
    #Updates screen continually
    pygame.display.flip()




main()
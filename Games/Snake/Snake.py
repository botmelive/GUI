import pygame
import time
import random

pygame.init()

display_width  = 800
display_height = 600

white = (255,255,255)
gray = (50,50,60)
silver = (192,192,192)
gray_obj = (120,120,120)

gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
pygame.display.set_caption('PY-Game')

smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 34)
largefont = pygame.font.SysFont('comicsansms', 50)

def message_to_screen(msg,color,y_displace = 0,size = "small"):
    textSurf,textReact = text_objects(msg,color)
    textRect.center = (display_width/2),((display_heigth/2)+y_displace)


def snake(block_size,snakelist):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay,silver,[XnY[0],XnY[1],block_size,block_size])
    

def game_intro():
    intro = True

    while intro:
        gameDisplay.fill(white)
        message_to_screen("Welcome To PY-Game",gray_obj,-100,"large")
        message_to_screen('Lets Get Started',gray,-30)
        pygame.display.update()
        clock.tick(15)

def text_objects(text,color,size = 'small'):
    if size == "small":
        textSurface = smallfont.render
    elif size == "medium":
        textSurface = medfont.render
    elif size == "large":
        textSurface = largefont.render
        
    return textSurface,textSurface.get_rect() 

def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2
    block_size = 10
    n = 5
    lead_x_change = 0
    lead_y_change = 0
    snakelist = []
    snakelength = 1
    block_movement = 5
    randobjx = round(random.randrange(0,display_width - block_size - 20)/10.0)*10.0
    randobjy = round(random.randrange(0,display_height - block_size - 20)/10.0)*10.0
    
    while not gameExit:
        
        while gameOver == True:
            gameDisplay.fill(gray)
            message_to_screen("Game Over,Press C to Play or Q to Quit",
                              white,
                              y_displace = -50,
                              size = "large")
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.key == pygame.K_q:
                    gameExit = True
                    gameOver = False
                    
                if event.key == pygame.K_c:
                    gameLoop()    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_movement
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_movement
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_movement
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_movement
                    lead_x_change = 0

            if lead_x >= display_width + 12 or lead_x < 0 or lead_y >= display_height -12 or lead_y < 0: #Check whether snake is within boundary
                gameOver = True    
                    
        lead_x += lead_x_change
        lead_y += lead_y_change
        randobjthickness = block_size
        gameDisplay.fill(gray)
        pygame.draw.rect(gameDisplay,gray_obj,[randobjx,randobjy, randobjthickness,randobjthickness])  #Draws the random object

        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)
        
        if len(snakelist) > snakelength:
            del snakelist[0]

        for eachsegment in snakelist[:-1]:
            if eachsegment == snakehead:
                gameOver = True
        
        snake(block_size,snakelist)

        pygame.display.update()

        '''if lead_x >= randobjx and lead_x <= randobjx + randobjthickness:
            if lead_y >= randobjy and lead_y <= randobjy + randobjthickness:
               randobjx = round(random.randrange(0,display_width - block_size)/10.0)*10.0
               randobjy = round(random.randrange(0,display_height - block_size)/10.0)*10.0
               snakelength += 1'''

        if lead_x > randobjx and lead_x < randobjx + randobjthickness or lead_x + block_size > randobjx and lead_x + block_size < randobjx + randobjthickness:
            if lead_y > randobjy and lead_y < randobjy + randobjthickness:
                randobjx = round(random.randrange(0,display_width - block_size))
                randobjy = round(random.randrange(0,display_height - block_size))
                snakelength += 1
            elif lead_y + block_size > randobjy and lead_y + block_size < randobjy + randobjthickness:
                randobjy = round(random.randrange(0,display_height - block_size))
                randobjx = round(random.randrange(0,display_width - block_size))
                snakelength += 1
          
        if snakelength > n:
            block_movement += 1
            n = n+3
               
        clock.tick(30)
        
        
            
    pygame.quit()

game_intro()
gameLoop()       

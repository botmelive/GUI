### Made by Joshua ###
import pygame,time
from random import randint,choice
#import sys

pygame.init()
#log = open('Log.txt','w')
#sys.stdout = log

##CONSTANTS

##Color Constants

#           R    G   B
PURPLE  = ( 48, 10, 36)
GREEN   = (000,255,000)
COMBLUE = (212,222,255)
ORANGE  = (200, 41, 83)
GRAY    = ( 50, 50, 60)
CYAN    = (255, 10,255)
PINK    = (119, 52, 90)
RED     = (255,  0,  0)

##Game Constants
GAMETITLE = 'Invaders'
DISPLAYWIDTH = 800
DISPLAYHEIGHT = 600
BGCOLOR = PURPLE
X_MARGIN = 30
Y_MARGIN = 30
FPS = 60

##Player Constants
PLAYERWIDTH = 50
PLAYERHEIGHT = 7
PLAYERSPEED = 7
PLAYERCOLOR = GREEN
PLAYERNAME = 'Player'

##Bullet Constants
BULLETWIDTH = 5
BULLETHEIGHT = 5
BULLETCOLOR = CYAN
BULLETSPEED = 15

##Alien Constants
ALIENHEIGHT = 25
ALIENWIDTH = 25
ALIENSPEED = 8
ALIENROW = 10
ALIENCOLOUMN = 3
ALIENGAP_Y = ALIENHEIGHT + 45
ALIENGAP_X = ALIENWIDTH + 45
ALIENNAME = 'Alien'
ALIENTYPE = ['Blue','White','Green']

##Blocker Constants
BLOCKERHEIGHT = 10
BLOCKERWIDTH = 10
BLOCKERCOLOR = GREEN
BLOCKERGAP = 10

##Initialize Game
Display = pygame.display.set_mode((DISPLAYWIDTH,DISPLAYHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(GAMETITLE)
icon = pygame.image.load('images/enemy1_1.png')
pygame.display.set_icon(icon)
Display.fill(BGCOLOR)
lasersound = pygame.mixer.Sound('laser.ogg')
smallfont = pygame.font.SysFont("orena", 20)
medfont = pygame.font.SysFont("orena", 25)
largefont = pygame.font.SysFont("orena", 30)
numfontsmall = pygame.font.SysFont("fonts/space_invaders.ttf",35)
numfontmedium = pygame.font.SysFont('fonts/space_invaders.ttf',40)
wallpaper = pygame.image.load('images/background.jpg')

class Player:
	def __init__(self,posx,posy,color,size=(PLAYERHEIGHT,PLAYERWIDTH)):
		self.alive = True
		self.x = posx
		self.y = posy
		self.color = color
		self.width = size[0]
		self.height = size[1]
	def render(self):
		pygame.draw.rect(Display,self.color,[self.x,self.y,self.height,self.width])

	def isalive(self):
		return self.alive

class Bullet:
	def __init__(self,posx,posy,color,speed=BULLETSPEED,size=(BULLETWIDTH,BULLETHEIGHT)):
		self.x = posx 
		self.y = posy
		self.color = color
		self.width = size[0]
		self.height = size[1]
		self.speed = speed

	def render(self):
		pygame.draw.rect(Display,self.color,[self.x,self.y,self.height,self.width])

class Alien:
	def __init__(self,posx,posy,image_no,alientype,size=(ALIENWIDTH,ALIENHEIGHT)):
		self.x = posx 
		self.y = posy
		self.width = size[0]
		self.height = size[1]
		self.image = []
		self.type = alientype
		if image_no == 0:
		    self.image.append(pygame.image.load('images/enemy1_1.png'))
		    self.image.append(pygame.image.load('images/enemy1_2.png'))
		elif image_no == 1:
			self.image.append(pygame.image.load('images/enemy2_1.png'))
			self.image.append(pygame.image.load('images/enemy2_2.png'))
		elif image_no == 2:
			self.image.append(pygame.image.load('images/enemy3_1.png'))
			self.image.append(pygame.image.load('images/enemy3_2.png'))
		else:
			self.image.append(pygame.image.load('images/enemy2_1.png'))
			self.image.append(pygame.image.load('images/enemy2_2.png'))

		self.image[0].convert_alpha()
		self.image[1].convert_alpha()
		self.image[0] = pygame.transform.scale(self.image[0],(self.width,self.height))
		self.image[1] = pygame.transform.scale(self.image[1],(self.width,self.height))

	def render(self,img=0):
		#pygame.draw.rect(Display,PLAYERCOLOR,[self.x,self.y,self.height,self.width],2)
		Display.blit(self.image[img],(self.x, self.y))


def intersect(s1_x, s1_y, s2_x, s2_y, height, width):
	if(s1_x > s2_x - width) and (s1_x < s2_x + width) and (s1_y>s2_y - height) and (s1_y<s2_y + height):
		return True
	else:
		return False


def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (DISPLAYWIDTH / 2), (DISPLAYHEIGHT / 2)+y_displace
    Display.blit(textSurf, textRect)

def score(msg,y_displace):
	text = msg
	textSurface = numfontsmall.render(text,True,GREEN)
	textRect = textSurface.get_rect()
	textRect.center = (DISPLAYWIDTH / 2), (DISPLAYHEIGHT / 2)+y_displace
	Display.blit(textSurface, textRect)

def live_score(pts):
	text = '{}'.format(pts)
	textSurface = numfontmedium.render(text,True,GREEN)
	textRect = textSurface.get_rect()
	textRect.center = (X_MARGIN, Y_MARGIN)
	Display.blit(textSurface, textRect)

def pause():
	paused = True
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					paused = False
					break
		Display.blit(wallpaper,(0,0))
		message_to_screen('Paused',GRAY,-40,'large')
		message_to_screen('Press P to play',GREEN,10,'medium')
		pygame.display.update()

def gameintro():
	intro = True
	global gameover
	bullets = []
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					gameover = False
					intro = False
					break
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
		'''
		posx = randint(10,DISPLAYWIDTH)
		bullets.append(Bullet(posx,0,PINK))
		i = 0
		while i < len(bullets):
			if bullets[i].y > DISPLAYHEIGHT:
				del(bullets[i])
			i += 1

		for bullet in bullets:
			bullet.y += 2
		'''

		Display.blit(wallpaper,(0,0))

		#for bullet in bullets:
			#bullet.render()
		message_to_screen("Welcome to Invaders",GREEN,-50,'large')
		message_to_screen("Press P to Play or Q to quit",COMBLUE,0,"small")
		pygame.display.update()


def gameover_screen(time_player,alien_win,player_win):
	outro = True
	start = time.time()
	while outro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					outro = False
					break
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		Display.blit(wallpaper,(0,0))
		message_to_screen("Game Over",PINK,-100,"medium")
		wonmessage = '{} won'.format(win)
		message_to_screen(wonmessage,COMBLUE,-50,"small")
		msg = '{}: {} {}: {}'.format(ALIENNAME,alien_win,PLAYERNAME,player_win)
		score(msg,0)
		pygame.display.update()
		end = time.time()
		if (end - start) > 2:
			outro = False
			break

gameexit = False
alien_win = 0
player_win = 0
highscore = 0

while not gameexit:
	##Initialize Player
	player_x = (DISPLAYWIDTH-X_MARGIN)/2
	player_y = (DISPLAYHEIGHT-Y_MARGIN)
	player = Player(player_x, player_y, PLAYERCOLOR)
	player_x_change = 0
	player_life = 5

	##Initialize Alien
	alien = []
	alienpox = X_MARGIN
	alienpoy = Y_MARGIN
	x_offset = 35 
	AlienChange_y = 0
	for j in range(ALIENCOLOUMN):
		for i in range(ALIENROW):
			alien.append(Alien(alienpox + i*ALIENGAP_X + x_offset, alienpoy,j,ALIENTYPE[j]))
		alienpoy += ALIENGAP_Y
	    #x_offset += ALIENWIDTH + 10

	##Initialize Bullet
	bullet = []
	#background = []
	alienbullet = []

	gameover = True
	win = ALIENNAME
	current_time = time.time()
	last_moved_time = time.time()
	gamestarttime = time.time()
	lastfiredalien = time.time()
	points = 0
	looptime = []

	gameintro()
	while not gameover:
		loopstarttime = time.time()
	    ##Get Event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player_x_change += -PLAYERSPEED
				if event.key == pygame.K_RIGHT:
					player_x_change += PLAYERSPEED
				if event.key == pygame.K_SPACE:
					#lasersound.play()
					bullet.append(Bullet(player.x + 15,player.y,BULLETCOLOR))
				if event.key == pygame.K_p:
					pause()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					player_x_change = 0
				if event.key == pygame.K_RIGHT:
					player_x_change = 0

		current_time = time.time()

		if len(alien) == 0:
			win = PLAYERNAME
			gameover = True
			break
		
		#Set Alien Speed(Orientation)
		if (alien[len(alien)-1].x > DISPLAYWIDTH - X_MARGIN - 50):
			ALIENSPEED = -ALIENSPEED
			AlienChange_y = ALIENHEIGHT
		elif alien[0].x < X_MARGIN:
			ALIENSPEED = -ALIENSPEED
			AlienChange_y = ALIENHEIGHT

	    #Set Bullet Position
		for bullets in bullet:
			bullets.y += -BULLETSPEED

		
		itter = 0
		while itter < len(bullet):
			if bullet[itter].y < 0:
				del(bullet[itter])
			itter += 1

		### ALIEN BULLET AI ###

		if len(alien) != 0:
			alienb_pos = alien.index(choice(alien))

		if current_time - lastfiredalien > 2:
			#print(alienb_pos)
			#print(len(alienbullet))
			lastfiredalien = time.time()
			alienbullet.append(Bullet(alien[alienb_pos].x,alien[alienb_pos].y,ORANGE,8))

		#Check Bullet intersection with player
		for abullet in alienbullet:
			#print('Bullet intersect loop')
			if intersect(abullet.x,abullet.y,player.x,player.y,PLAYERHEIGHT,PLAYERWIDTH):
				player_life -= 1
				points += -500

		for abullets in alienbullet:
			#print('Bullet speed set loop')
			abullets.y += abullet.speed

		itter = 0
		while itter < len(alienbullet):
			#print('Bullet delete loop')
			if alienbullet[itter].y > DISPLAYHEIGHT:
				del(alienbullet[itter])
			itter += 1
		### END ALIEN BULLET AI ###

		#Check Bullet Intersection with Alien
		k,i = 0,0
		hit_bullet = []
		hit_alien = []
		for bullets in bullet:
			i = 0
			for aliens in alien:
				if intersect(bullets.x,bullets.y,aliens.x,aliens.y,ALIENHEIGHT,ALIENWIDTH):
					hit_alien.append(i)
					hit_bullet.append(k)
				i += 1
			k += 1

		hit_alien = list(set(hit_alien))
		hit_bullet = list(set(hit_bullet))

		for i in hit_bullet:
			del(bullet[i])

		for i in hit_alien:
			typ = alien[i].type
			if typ == 'Blue':
				points += 30
			elif typ == 'White':
				points += 20
			else:
				points += 10
			del(alien[i])
		
		#Set Player Position
		player_x += player_x_change
		player.x = player_x
		time_difference = current_time - last_moved_time

		#Set Alien Position
		if time_difference > 0.5:
			last_moved_time = time.time()
			for aliens in alien:
				aliens.image[0],aliens.image[1] = aliens.image[1],aliens.image[0]
				aliens.x += ALIENSPEED
				aliens.y += AlienChange_y

		for aliens in alien:
			if aliens.y >= player.y:
				win = ALIENNAME
				gameover = True
				break
		AlienChange_y = 0
		
		if player_life == 0:
			win = ALIENNAME
			gameover = True
		if player_life == 1:
			player.color = RED
		elif player_life == 3:
			player.color = ORANGE
		
		'''
		posx = randint(10,DISPLAYWIDTH)
		background.append(Bullet(posx,0,PINK))

		i = 0
		while i < len(background):
			if background[i].y > DISPLAYHEIGHT-20:
				del(background[i])
			i += 1

		for bullets in background:
			bullets.y += 8
		'''

		##Render 
		#Display.fill(BGCOLOR)
		Display.blit(wallpaper,(0,0))
		live_score(points)
		
		'''
		for bullets in background:
			bullets.render()
		'''
		player.render()
		for abullet in alienbullet:
			abullet.render()
		
		for bullets in bullet:
			bullets.render()

		for aliens in alien:
			aliens.render()	
		
		pygame.display.update()
		clock.tick(FPS)
		loopendtime = time.time()
		totaltime = loopendtime - loopstarttime
		looptime.append(totaltime)
		### End Game Loop 

	if win == 'Alien':
		alien_win += 1
	else:
		player_win += 1
	gameendtime = time.time()
	totalgametime = gameendtime - gamestarttime
	gameover_screen(totalgametime,alien_win,player_win)


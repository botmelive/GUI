import pygame,time
#import sys

print('Initializing')
pygame.init()
#log = open('Log.txt','w')
#sys.stdout = log

##CONSTANTS
print('Loading Resources')
##Color Constants

#           R    G   B
PURPLE  = ( 48, 10, 36)
GREEN   = (000,255,000)
COMBLUE = (233,232,255)
ORANGE  = (200, 41, 83)
GRAY    = ( 50, 50, 60)
CYAN     = (255, 10,255)

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

##Blocker Constants
BLOCKERHEIGHT = 10
BLOCKERWIDTH = 10
BLOCKERCOLOR = GREEN
BLOCKERGAP = 10

##Initialize Game
Display = pygame.display.set_mode((DISPLAYWIDTH,DISPLAYHEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption(GAMETITLE)
Display.fill(BGCOLOR)
lasersound = pygame.mixer.Sound('laser.ogg')

print('Initializing Resources')
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
	def __init__(self,posx,posy,image_no,size=(ALIENWIDTH,ALIENHEIGHT)):
		self.x = posx 
		self.y = posy
		self.width = size[0]
		self.height = size[1]
		if image_no == 0:
		    self.image = pygame.image.load('alien1.png')
		elif image_no == 1:
			self.image = pygame.image.load('alien2.png')
		elif image_no == 2:
			self.image = pygame.image.load('alien3.png')
		else:
			self.image = pygame.image.load('alien1.png')

		self.image.convert_alpha()
		self.image = pygame.transform.scale(self.image,(self.width,self.height))
	def render(self):
		#pygame.draw.rect(Display,self.color,[self.x,self.y,self.height,self.width])
		Display.blit(self.image,(self.x, self.y))


def intersect(s1_x, s1_y, s2_x, s2_y, height, width):
	if(s1_x > s2_x - width) and (s1_x < s2_x + width) and (s1_y>s2_y - height) and (s1_y<s2_y + height):
		return True
	else:
		return False 

print('Initializing Player')
##Initialize Player
player_x = (DISPLAYWIDTH-X_MARGIN)/2
player_y = (DISPLAYHEIGHT-Y_MARGIN)
player = Player(player_x, player_y, PLAYERCOLOR)
player_x_change = 0

print('Initializing Alien')
##Initialize Alien
alien = []
alienpox = X_MARGIN
alienpoy = Y_MARGIN
x_offset = 35 
AlienChange_y = 0
for j in range(ALIENCOLOUMN):
	for i in range(ALIENROW):
		alien.append(Alien(alienpox + i*ALIENGAP_X + x_offset, alienpoy,j))
	alienpoy += ALIENGAP_Y
	#x_offset += ALIENWIDTH + 10


print('Final Loading')
##Initialize Bullet
bullet = []

gameover = False
current_time = time.time()
last_moved_time = time.time()
gamestarttime = time.time()

print('''
FPS set to {}
Screen Resolution set to {} X {} '''.format(FPS,DISPLAYWIDTH,DISPLAYHEIGHT))

while not gameover:
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
				lasersound.play()
				bullet.append(Bullet(player.x + 15,player.y,BULLETCOLOR))

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				player_x_change = 0
			if event.key == pygame.K_RIGHT:
				player_x_change = 0

	if len(alien) == 0:
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
		del(alien[i])
	
	#Set Player Position
	player_x += player_x_change
	player.x = player_x
	current_time = time.time()
	time_difference = current_time - last_moved_time

	#Set Alien Position
	if time_difference > 0.5:
		last_moved_time = time.time()
		for aliens in alien:
			aliens.x += ALIENSPEED
			aliens.y += AlienChange_y

	for aliens in alien:
		if aliens.y >= player.y:
			gameover = True
			break

	AlienChange_y = 0
	
	##Render 
	Display.fill(BGCOLOR)
	player.render()

	for bullets in bullet:
		bullets.render()

	for aliens in alien:
		aliens.render()	
	
	pygame.display.update()
	clock.tick(FPS)
gameendtime = time.time()

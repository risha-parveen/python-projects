import pygame
import os
pygame.font.init() #initiates pygame font library
pygame.mixer.init()

WIDTH, HEIGHT =800,400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH//2 -5 , 0, 10, HEIGHT)
pygame.display.set_caption("Rocket game")

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT=pygame.font.SysFont('comicsans', 33)
WINNER_FONT=pygame.font.SysFont('comicsans', 90)

COLOR = (50,50,75)
FPS = 60
VEL =5
BULLET_VEL=7
MAX_BULLETS= 3

# represents the 2 players
YELLOW_HIT=pygame.USEREVENT +1
RED_HIT= pygame.USEREVENT +2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
	os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP= pygame.transform.rotate(
	pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55, 40)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
	os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP= pygame.transform.rotate(
	pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_background.png')),(WIDTH,HEIGHT))

def draw_window(yellow,red,red_bullets,yellow_bullets,red_health,yellow_health):
	WIN.blit(SPACE, (0,0))
	pygame.draw.rect(WIN, (0,0,0), BORDER)

	red_health_text= HEALTH_FONT.render("Health: "+ str(red_health), 1,(255,255,255) )
	yellow_health_text= HEALTH_FONT.render("Health: "+str(yellow_health), 1,(255,255,255))

	WIN.blit(red_health_text, (WIDTH-red_health_text.get_width()-10,10))
	WIN.blit(yellow_health_text, (10,10))
	WIN.blit(YELLOW_SPACESHIP ,(yellow.x, yellow.y) )
	WIN.blit(RED_SPACESHIP, (red.x,red.y))


	for bullet in red_bullets:
		pygame.draw.rect(WIN, (255,0,0), bullet)

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN, (255,255,0),bullet)

	pygame.display.update()

def draw_winner(text):
	draw_text=WINNER_FONT.render(text, 1, (200,255,250))
	WIN.blit(draw_text, (WIDTH/2 -draw_text.get_width()/2 , HEIGHT/2 - draw_text.get_height()/2))
	pygame.display.update()
	pygame.time.delay(4000) # to pause the game for 5 sec and restart the game

def yellow_handle_movement(keys_pressed, yellow):
	# here switching the values of spaceship width and height so that
	# it was interchanged during the process of rotation.
	if keys_pressed[pygame.K_a] and yellow.x - VEL >0: #left
		yellow.x-=VEL
	if keys_pressed[pygame.K_d] and yellow.x+VEL+40 < BORDER.x:
		yellow.x+=VEL
	if keys_pressed[pygame.K_w] and yellow.y - VEL >0:
		yellow.y-=VEL
	if keys_pressed[pygame.K_s] and yellow.y+VEL+55 < HEIGHT:
		yellow.y+=VEL

def red_handle_movement(keys_pressed, red):
	if keys_pressed[pygame.K_LEFT] and red.x- VEL> BORDER.x+ 10: # 10 is border width
		red.x-=VEL
	if keys_pressed[pygame.K_RIGHT] and red.x + VEL+40<WIDTH:
		red.x+=VEL
	if keys_pressed[pygame.K_UP] and red.y - VEL>0:
		red.y-=VEL
	if keys_pressed[pygame.K_DOWN] and red.y +VEL+55<HEIGHT:
		red.y+=VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
	for bullet in yellow_bullets:
		bullet.x+=BULLET_VEL
		if red.colliderect(bullet): #this function checks whether the bullet has collided with rocket
			# works only if both the objects are rectangles
			pygame.event.post(pygame.event.Event(RED_HIT))
			# post function exites the pygame.event.get() in the main function
			yellow_bullets.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet) #bullets should be removed so that the list becomes emptied

	for bullet in red_bullets:
		bullet.x-=BULLET_VEL
		if yellow.colliderect(bullet): 
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x <0:
			red_bullets.remove(bullet)

def main():
	clock = pygame.time.Clock()

	yellow = pygame.Rect(200, 200, 55,40)
	red = pygame.Rect(600, 200, 55 ,40)

	red_bullets=[]
	yellow_bullets=[]

	red_health= 10
	yellow_health=10

	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				exit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
					bullet= pygame.Rect(
						yellow.x + yellow.width,yellow.y+yellow.height//2-2, 10,5)
					yellow_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()

				if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
					bullet=pygame.Rect(
						red.x, red.y+red.height//2 -2 ,10,5)
					red_bullets.append(bullet)
					BULLET_FIRE_SOUND.play()

			if event.type == RED_HIT:
				red_health-=1
				BULLET_HIT_SOUND.play()

			if event.type == YELLOW_HIT:
				yellow_health-=1
				BULLET_HIT_SOUND.play()

		

		winner_text=""
		if red_health<=0:
			winner_text = "YELLOW WINS!"

		if yellow_health<=0:
			winner_text="RED WINS!"

		if winner_text!="":
			draw_winner(winner_text)
			break	
		
		keys_pressed= pygame.key.get_pressed()
		
		yellow_handle_movement(keys_pressed,yellow)
		red_handle_movement(keys_pressed, red)

		handle_bullets(yellow_bullets,red_bullets, yellow, red)

		draw_window(yellow,red,red_bullets,yellow_bullets,red_health,yellow_health)

	main()

if __name__ == "__main__":
	main()
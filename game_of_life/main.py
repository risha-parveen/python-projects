import pygame 

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME OF LIFE")

FPS= 60
BG_COLOR= (40,40,40)

def draw_window():
	WIN.fill(BG_COLOR)
	pygame.display.update()

def main():

	clock= pygame.time.Clock()
	run= True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run= False

		draw_window()

	pygame.quit()

if __name__=="__main__":
	main()
import pygame
import grid1

width, height = 600,400
size = (width, height)

pygame.init()
pygame.display.set_caption("CONWAY'S GAME OF LIFE")
WIN= pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 60

bg_color=(15,40,40)
color=(200,250,250)

scaler = 7
offset = 0.05

Grid = grid1.Grid(width,height, scaler, offset)
Grid.draw_array()

def main():
    run = True
    while run:
        clock.tick(fps)
        WIN.fill(bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        Grid.conway(bg_color=bg_color, color=color, surface=WIN)
        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()
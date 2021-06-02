import pygame
import numpy as np
import random

class Grid:
    def __init__(self, width, height, scaler, offset):
        self.scale=scaler
        self.rows=width//self.scale
        self.columns=height//self.scale
        self.size=(self.rows, self.columns)
        self.array=np.ndarray(shape=(self.size))
        self.offset=offset

    def draw_array(self):
        for x in range(self.rows):
            for y in range(self.columns):
                self.array[x][y]=random.randint(0,1)

    def get_neighbours(self,x,y):
        total=0
        for i in range(max(0,x-1),min(self.rows,x+2)):
            for j in range(max(0,y-1),min(self.columns,y+2)):
                if (x,y)==(i,j):
                    continue
                total+=self.array[i][j]
        return total
    
    def conway(self,bg_color,color,surface):
        
        for x in range(self.rows):
            for y in range(self.columns):
                x1 = x*self.scale
                y1 = y*self.scale
                if self.array[x][y]==1:
                    pygame.draw.rect(surface, color , [x1, y1,self.scale-self.offset,self.scale-self.offset])
                else:
                    pygame.draw.rect(surface, bg_color, [x1,y1, self.scale,self.scale])
        next=np.ndarray(shape=self.size)

        for x in range(self.rows):
            for y in range(self.columns):
                neighbours=self.get_neighbours(x,y)
                state=self.array[x][y]
                if state==0 and neighbours==3:
                    next[x][y]=1
                elif state==1 and (neighbours<2 or neighbours>3):
                    next[x][y]=0
                else:
                    next[x][y]=state
        self.array=next

    
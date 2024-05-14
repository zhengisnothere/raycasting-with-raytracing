# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:21:02 2023

@author: userid
"""

import pygame
from var_data import screen,tile_size


class Grid(pygame.sprite.Sprite):
    def __init__(self, shape, texture, index_x, index_y):
        super().__init__()
        self.index_x=index_x
        self.index_y=index_y
        self.shape=shape
        self.texture=texture
        self.image=pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        self.color=(0,255,0)
        self.rect=self.image.get_rect(topleft=(index_x*tile_size,index_y*tile_size))
        self.type_image()
        if self.texture=='portal':
            self.connected_portal=None
        
    def type_image(self):
        if self.texture=='wall':
            self.color=(0,255,0)
            if self.shape == 'big square':
                pygame.draw.rect(self.image, self.color, (0, 0, tile_size, tile_size))
            elif self.shape=='circle':
                pygame.draw.circle(self.image, self.color, (int(tile_size/2),int(tile_size/2)), int(tile_size/2))
            elif self.shape=='rect 1':
                pygame.draw.rect(self.image, self.color, (int(tile_size/4), 0, int(tile_size/2), tile_size))
            elif self.shape=='rect 2':
                pygame.draw.rect(self.image, self.color, (0, int(tile_size/4), tile_size, int(tile_size/2)))
            elif self.shape=='small square':
                pygame.draw.rect(self.image, self.color, (int(tile_size/2), int(tile_size/2), int(tile_size/2), int(tile_size/2)))
            
        if self.texture=='mirror':
            self.color=(0,0,255)
            if self.shape=='h':
                pygame.draw.line(self.image, self.color, (0,int(tile_size/2)), (tile_size,int(tile_size/2)))
            elif self.shape=='v':
                pygame.draw.line(self.image, self.color, (int(tile_size/2),0), (int(tile_size/2),tile_size))
            elif self.shape=='c':
                pygame.draw.circle(self.image, self.color, (int(tile_size/2),int(tile_size/2)), int(tile_size/2))
                
        if self.texture=='portal':
            self.color=(255,0,0)
            if self.shape=='h':
                pygame.draw.line(self.image, self.color, (int(tile_size/4),int(tile_size/2)), (int(tile_size/4*3),int(tile_size/2)))
            elif self.shape=='v':
                pygame.draw.line(self.image, self.color, (int(tile_size/2),int(tile_size/4)), (int(tile_size/2),int(tile_size/4*3)))
        
        self.mask = pygame.mask.from_surface(self.image)
        
    def draw(self):
        screen.blit(self.image, self.rect)
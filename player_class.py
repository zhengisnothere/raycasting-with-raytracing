# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:20:18 2023

@author: userid
"""

import pygame
import math
from var_data import tile_size,screen,screen_length,screen_width,map_length,map_width,show_text

class Player(pygame.sprite.Sprite):
    def __init__(self, grid_map):
        super().__init__()
        self.image=pygame.Surface((4,4))
        self.image.fill((0,0,255))
        self.rect=self.image.get_rect(topleft=(0,0))
        self.mask=pygame.mask.from_surface(self.image)
        self.old_x=0
        self.old_y=0
        self.dir=0
        self.speed=4
        self.grid_map=grid_map
        
    def draw(self):
        screen.blit(self.image, self.rect)
        self.show_dir()
        
    def movement(self):
        key=pygame.key.get_pressed()
        x=self.rect.x
        y=self.rect.y
        if key[pygame.K_w]:
            x+=math.cos(math.radians(self.dir))*self.speed
            y-=math.sin(math.radians(self.dir))*self.speed
        elif key[pygame.K_s]:
            x-=math.cos(math.radians(self.dir))*self.speed
            y+=math.sin(math.radians(self.dir))*self.speed
        if key[pygame.K_a]:
            x+=math.cos(math.radians(self.dir+90))*self.speed
            y-=math.sin(math.radians(self.dir+90))*self.speed
        elif key[pygame.K_d]:
            x+=math.cos(math.radians(self.dir-90))*self.speed
            y-=math.sin(math.radians(self.dir-90))*self.speed
        self.rect.x=max(0,min(screen_length,x))
        self.rect.y=max(0,min(screen_width,y))
        
    
    def set_direction(self):
        mouse_x_move=pygame.mouse.get_rel()[0]
        self.dir+=mouse_x_move*-0.5
        self.dir%=360
        
    def show_dir(self):
        front_x=self.rect.x+math.cos(math.radians(self.dir))*10
        front_y=self.rect.y-math.sin(math.radians(self.dir))*10
        pygame.draw.line(screen, (255,0,255), (self.rect.x,self.rect.y), (front_x,front_y))
        
    def portal_collision(self):
        ix=max(0,min(map_length-1,int(self.rect.x/tile_size)))
        iy=max(0,min(map_width-1,int(self.rect.y/tile_size)))
        c_grid=self.grid_map.matrix[iy][ix]
        if c_grid.texture=='portal':
            connect_portal=c_grid.connected_portal
            collision=self.mask.overlap(c_grid.mask, (c_grid.rect.x-self.rect.x,c_grid.rect.y-self.rect.y))
            if collision:
                enter_dir=math.degrees(math.atan2(self.old_y-self.rect.y, self.rect.x-self.old_x))%360
                bx=self.rect.x-c_grid.rect.centerx
                by=self.rect.y-c_grid.rect.centery
                self.rect.x=connect_portal.rect.centerx-bx
                self.rect.y=connect_portal.rect.centery+by
                x=self.rect.x
                y=self.rect.y
                while self.mask.overlap(connect_portal.mask, (connect_portal.rect.x-self.rect.x,connect_portal.rect.y-self.rect.y)):
                    x+=math.cos(math.radians(enter_dir))*self.speed
                    y-=math.sin(math.radians(enter_dir))*self.speed
                    self.rect.x=max(0,min(screen_length,x))
                    self.rect.y=max(0,min(screen_width,y))
                    
        
    def update(self):
        self.old_x=self.rect.x
        self.old_y=self.rect.y
        self.set_direction()
        self.movement()
        self.portal_collision()

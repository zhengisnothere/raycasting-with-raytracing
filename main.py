# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:19:58 2023

@author: userid
"""
import pygame
import sys

from var_data import screen,show_text

from raycaster_class import Raycaster
from player_class import Player
from grid_map_class import Grid_Map

clock=pygame.time.Clock()

grid_map=Grid_Map()
player=Player(grid_map)
raycaster=Raycaster(player,grid_map)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    mouse_x,mouse_y=pygame.mouse.get_pos()
    player.update()
    grid_map.update()
    
    screen.fill((0,0,0))
    # grid_map.draw()
    # player.draw()
    raycaster.draw()
    show_text(str(player.dir), (0,10))
    show_text(str(int(clock.get_fps())), (0,0))
    
    pygame.display.flip()
    clock.tick(30)
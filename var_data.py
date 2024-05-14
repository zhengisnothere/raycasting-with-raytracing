# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 18:04:54 2023

@author: userid
"""
import pygame

pygame.init()

map_length=10
map_width=10
tile_size=36
screen_length=map_length*tile_size
screen_width=map_width*tile_size
screen=pygame.display.set_mode((screen_length,screen_width))
pygame.display.set_caption('hello world')
show_font = pygame.font.SysFont("monospace", 15)

def show_text(text,pos):
    text_image=show_font.render(text, 1, (255,255,255))
    screen.blit(text_image, pos)
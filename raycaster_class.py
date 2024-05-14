# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 11:01:42 2023

@author: Zheng
"""
import pygame
import math
from var_data import screen_length,screen_width, screen, map_length, map_width, tile_size

class Raycaster(pygame.sprite.Sprite):
    def __init__(self, player, grid_map):
        super().__init__()
        self.image=pygame.Surface((1,1))
        self.image.fill((0,255,255))
        self.rect=self.image.get_rect()
        self.mask=pygame.mask.from_surface(self.image)
        self.max_distance=200
        self.x=0
        self.y=0
        self.speed=1
        self.fov=30
        self.res=6
        self.player=player
        self.grid_map=grid_map
    
    def draw(self):
        self.raycast()
       
    def draw_wall_line(self,fov_dir,draw_distance,color_base='g', color=None): 
        draw_x=int(screen_length/2)-fov_dir*self.res
        draw_distance=draw_distance*math.cos(math.radians(fov_dir))
        half_wall_height=int(3000/draw_distance)
        draw_start_y=int(screen_width/2)-half_wall_height
        draw_end_y=int(screen_width/2)+half_wall_height
        if color is None:
            brightness=-(255/self.max_distance)*draw_distance+255
            if color_base=='r':
                color=(brightness,0,0)
            elif color_base=='g':
                color=(0,brightness,0)
            elif color_base=='b':
                color=(0,0,brightness)
            elif color_base=='w':
                color=(brightness,brightness,brightness)
        pygame.draw.line(screen,color,(draw_x,draw_start_y),(draw_x,draw_end_y),self.res)
       
    def move(self,move_dir):
        step_x = math.cos(math.radians(move_dir))*self.speed
        step_y = math.sin(math.radians(move_dir))*self.speed
        self.x+=step_x
        self.y-=step_y
        self.rect.x=self.x
        self.rect.y=self.y
       
    def raycast(self):
        player=self.player
        for fov_dir in range(-self.fov,self.fov+1): #-self.fov,self.fov+1
            self.rect.x,self.rect.y=(player.rect.centerx,player.rect.centery)
            self.x,self.y=self.rect.x,self.rect.y
            move_dir=fov_dir+player.dir
            draw_distance=0
            touch_wall=False
            ray_reflected=0
            ray_tp=0
            reflected_dis=[]
            tp_dis=[]
            points=[(player.rect.centerx,player.rect.centery)]
            while draw_distance<self.max_distance:
                draw_distance+=1
                ix=max(0,min(map_length-1,int(self.rect.x/tile_size)))
                iy=max(0,min(map_width-1,int(self.rect.y/tile_size)))
                c_grid=self.grid_map.matrix[iy][ix]
                if self.mask.overlap(c_grid.mask, (c_grid.rect.x-self.rect.x,c_grid.rect.y-self.rect.y)):
                    if c_grid.texture=='wall':
                        touch_wall=True
                        break
                    if c_grid.texture=='mirror':
                        #反射：第一个反射点反向延长总距离
                        points.append((self.rect.x,self.rect.y))
                        ray_reflected+=1
                        reflected_dis.append(draw_distance)
                        mirror_shape=c_grid.shape
                        if mirror_shape=='h':
                            move_dir=360-move_dir
                        elif mirror_shape=='v':
                            move_dir%=360
                            if 360>=move_dir>=180:
                                move_dir=540-move_dir
                            else:
                                move_dir=180-move_dir
                        elif mirror_shape=='c':
                            x1=self.rect.x
                            y1=self.rect.y
                            x0=c_grid.rect.centerx
                            y0=c_grid.rect.centery
                            move_dir%=360
                            normal_line_dir=math.degrees(math.atan2(y0-y1, x1-x0))%360
                            i_angle=move_dir-(normal_line_dir+180)%360
                            reflected_dir=normal_line_dir-i_angle
                            move_dir=reflected_dir%360
                            while self.mask.overlap(c_grid.mask, (c_grid.rect.x-self.rect.x,c_grid.rect.y-self.rect.y)):
                                self.move(move_dir)
                    if c_grid.texture=='portal':
                        points.append((self.rect.x,self.rect.y))
                        ray_tp+=1
                        tp_dis.append(draw_distance)
                        connect_portal=c_grid.connected_portal
                        #tp
                        bx=self.rect.x-c_grid.rect.centerx
                        by=self.rect.y-c_grid.rect.centery
                        self.rect.x=connect_portal.rect.centerx-bx
                        self.rect.y=connect_portal.rect.centery+by
                        self.x=self.rect.x
                        self.y=self.rect.y
                        points.append((self.rect.x,self.rect.y))
                    
                self.move(move_dir)
                            
            points.append((self.rect.x,self.rect.y))
            # pygame.draw.lines(screen, (255,255,255), 0, points)
            
            # draw 3d lines
            if touch_wall:
                self.draw_wall_line(fov_dir, draw_distance)
            
            if ray_reflected>0:
                for index in range(ray_reflected):
                    dis=reflected_dis[index]
                    dis=dis*math.cos(math.radians(fov_dir))
                    color=-(255/self.max_distance)*dis+255
                    draw_x=int(screen_length/2)-fov_dir*self.res
                    half_wall_height=int(3000/dis)
                    draw_start_y=int(screen_width/2)-half_wall_height
                    draw_end_y=int(screen_width/2)+half_wall_height
                    pygame.draw.line(screen, (color,color,color), (draw_x,draw_start_y), (draw_x,draw_start_y+half_wall_height*0.02),self.res)
                    pygame.draw.line(screen, (color,color,color), (draw_x,draw_end_y), (draw_x,draw_end_y-half_wall_height*0.02),self.res)
                
            if ray_tp>0:
                for index in range(ray_tp):
                    dis=tp_dis[index]
                    dis=dis*math.cos(math.radians(fov_dir))
                    color=-(255/self.max_distance)*dis+255
                    draw_x=int(screen_length/2)-fov_dir*self.res
                    half_wall_height=int(3000/dis)
                    draw_start_y=int(screen_width/2)-half_wall_height
                    draw_end_y=int(screen_width/2)+half_wall_height
                    pygame.draw.line(screen, (color,0,0), (draw_x,draw_start_y), (draw_x,draw_start_y+half_wall_height*0.02),self.res)
                    pygame.draw.line(screen, (color,0,0), (draw_x,draw_end_y), (draw_x,draw_end_y-half_wall_height*0.02),self.res)
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:21:51 2023

@author: userid
"""
import random
from grid_class import Grid
from var_data import map_length,map_width


class Grid_Map:
    def __init__(self):
        shape={'blank':[''],
               'wall':['big square','small square','rect 1','rect 2','circle'],
               'mirror':['h','v','c'],
               'portal':['h','v']}
        texture=['blank','blank','wall','wall','mirror','mirror','portal']
        self.matrix=[]
        portals=[]
        for iy in range(map_width):
            row=[]
            for ix in range(map_length):
                chosen_texture=random.choice(texture)
                chosen_shape=random.choice(shape[chosen_texture])
                if chosen_texture=='portal':
                    portals.append((ix,iy))
                row.append(Grid(chosen_shape, chosen_texture, ix, iy))
            self.matrix.append(row)
        for i in portals:
            npx,npy=0,0
            this_portal=self.matrix[i[1]][i[0]]
            while self.matrix[npy][npx].texture=='portal':
                npx=random.randint(0, map_length-1)
                npy=random.randint(0, map_width-1)
            new_portal=Grid(this_portal.shape, 'portal', npx, npy)
            self.matrix[npy][npx]=new_portal
            this_portal.connected_portal=new_portal
            new_portal.connected_portal=this_portal
                
    def draw(self):
        for row in self.matrix:
            for grid in row:
                grid.draw()
            
    def update(self):
        for row in self.matrix:
            for grid in row:
                grid.update()
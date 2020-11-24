# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 16:34:30 2020

@author: Maud
"""

import numpy as np

def create_target_positions(size = None, sf = 1.4): 
    r = 1.5
    target_left_positions = np.empty([int(size/2), 2])
    target_right_positions = np.empty([int(size/2), 2])
    t = np.random.uniform(0, 1, size=size)
    u = np.random.uniform(0, 1, size=size)
    y = r*np.sqrt(t) * np.sin(2*np.pi*u)
    x = r*np.sqrt(t) * np.cos(2*np.pi*u)
    x = np.round(x, 1)
    y = np.round(y, 1)
    #Make sure the positions in the grating are always the same, so visibility is always the same     
    sf = sf
    target0_x = np.array([-sf/4*4, -sf/4*2, -sf/4*0, sf/4*2, sf/4*4]) 
    for i in range(x.shape[0]): 
        if x[i] <= np.mean(target0_x[0:2]): 
            x[i] = target0_x[0]
        elif x[i] <= np.mean(target0_x[1:3]): 
            x[i] = target0_x[1]
        elif x[i] <= np.mean(target0_x[2:4]): 
            x[i] = target0_x[2]
        elif x[i] <= np.mean(target0_x[3:5]): 
            x[i] = target0_x[3]
        else: 
            x[i] = target0_x[4]
    target_left_positions[:, 0] = x[0:int(size/2)] - 5
    target_left_positions[:, 1] = y[0:int(size/2)]
    target_right_positions[:, 0] = x[int(size/2):] + 5
    target_right_positions[:, 1] = y[int(size/2):]
    
    return target_left_positions, target_right_positions

t_left_pos, t_right_pos = create_target_positions(size = 84, sf = 1.4)

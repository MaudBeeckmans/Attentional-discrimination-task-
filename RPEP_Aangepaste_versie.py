# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 22:12:36 2020

@author: Maud
"""

import numpy as np
"""
To be defined in the creation of the Design_array:
    - FTI x flashpos x targetpos possible combinations
    - Grating_startT (range = 500 - 600 ms)
    - Grating_FlashT (range = 750 - 1250 ms)
    - Target_positions
!: should start counting the frames from 0 (first frame = 0)
"""
#This part already works!
def create_design(n_blocks = 1): 
    for i in range(n_blocks): 
        Target_relative_position= np.array([0, 1])      #0 = same, 1 = opposite
        Flash_position = np.array([0, 1])        #0 = left, 1 = right
        FTI = np.arange(-15, 48, 3)
        Fixed_block = np.array(np.meshgrid(FTI, Flash_position, Target_relative_position)).T.reshape(-1,3)  #shape = (84, 3)
        n_blocktrials = Fixed_block.shape[0]
        np.random.shuffle(Fixed_block)
        if i == 0: 
            Fixed_blocks = Fixed_block
        else: 
            Fixed_blocks = np.concatenate([Fixed_blocks, Fixed_block])
    n_trials = n_blocks * n_blocktrials
    return Fixed_blocks, n_blocktrials, n_trials

Fixed_blocks, n_blocktrials, n_trials = create_design(n_blocks = 6)

#%%


def create_design_complete(Basic_array = None, n_trials = 1, n_blocktrials = 1, 
                           n_blocks = 1): 
    CorResp = np.array([Basic_array[:, 1] != Basic_array[:, 2]]).reshape(n_trials, 1)*1
    Target_position = np.copy(CorResp)
    #Count the blocks
    Block_count = np.repeat(np.arange(n_blocks), n_blocktrials).reshape(n_trials, 1)
    framerate = 1000/60         #time for 1 frame in ms (16,6666668)
    Grating_start_limits_ms = np.array([500, 600+framerate])        #+framerate since the upper boundary isn't included
    Grating_flash_limits_ms = np.array([750, 1250+framerate])       #in calculations with np.random.randint()
    Flash_duration = 2          #Moet achteraf nog bepaald worden!!!!
    Target_duration = 2         #Moet achteraf nog bepaald worden!!!!
    Grating_start_limits = np.round(Grating_start_limits_ms/framerate, 0)
    Grating_start_limits.astype(int)
    Grating_flash_limits = np.round(Grating_flash_limits_ms / framerate, 0)
    Grating_flash_limits.astype(int)
    #Create the arrays that contain the important timings & values for each trial (random)
    Grating_start_array = np.random.randint(Grating_start_limits[0], Grating_start_limits[1], n_trials)
    Grating_flash_array = np.random.randint(Grating_flash_limits[0], Grating_flash_limits[1], n_trials)
    Design_array = np.column_stack([Block_count, Fixed_block, CorResp, Target_position, Grating_start_array, Grating_flash_array])
    
    
    
    return Design_array, n_blocktrials, n_trials

Design_array, n_blocktrials, n_trials = create_design(n_blocks = 6)
        
    
    
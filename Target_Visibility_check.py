"""
Script made since I thought target wasn't always visible at each trial and not due to attention limits, but due to actual invisibility. 
This script shows that this is the case: when both target & gratingA have the same spatial frequency, there are locations at which the target is 
completely invisible (when it is located right in the middle of a white part I think). By changing the spatial frequency the target becomes visible at 
every location, however quite some variability int he amount of visibility based on the location remains. I wonder whether this might cause a problem 
for our experiment. Since detection accuracy might then differ based on target location instead of on the visual attentional properties. 
('target location' here always refers to location inside the grating, not L or R) 


Some information: 
* going to the next 'position' of the target via pressing 'f' or 'j'
* there are now 84 random positions displayed, only the left grating is displayed 
* you can quit the experiment pressing 'escape'
* sf is now put at 5, when put at 1.4 you can see that the target sometimes completely disappears 
"""

import numpy as np
import math, time, os, pandas
from psychopy import visual, data, core, event, gui



#B. Create the fixation point with function                                     Fixation point
#create the fixation point              #check whether the variables are important (maybe for formula)

win = visual.Window(fullscr = True, monitor = 'Laptop', units = 'deg')

# E. Create the Target                                                          Target
def create_target_positions(size = None): 
    r = 1.5
    target_left_positions = np.empty([int(size/2), 2])
    target_right_positions = np.empty([int(size/2), 2])
    t = np.random.uniform(0, 1, size=size)
    u = np.random.uniform(0, 1, size=size)
    y = r*np.sqrt(t) * np.sin(2*np.pi*u)
    x = r*np.sqrt(t) * np.cos(2*np.pi*u)
    x = np.round(x, 1)
    y = np.round(y, 1)
    target_left_positions[:, 0] = x[0:int(size/2)] - 5
    target_left_positions[:, 1] = y[0:int(size/2)]
    target_right_positions[:, 0] = x[int(size/2):] + 5
    target_right_positions[:, 1] = y[int(size/2):]
    return target_left_positions, target_right_positions

target_template =visual.GratingStim(win=win,tex='sin', mask='gauss',ori=0, sf=5, pos=(1,1), size= (1,1), interpolate=False)
left_count = 0
right_count = 0
def target_prepare(target_loc = None, amplitude = 25, left_i = left_count, right_i = right_count):         #target location: '0.0' = L, '1.0' = R
                                                                                                        #corresponds with trial['Target_hemifield']
    if target_loc == 0: 
        target_position = t_left_pos[left_i, :]
    else: 
        target_position = t_right_pos[right_i, :]
    target_template.pos = target_position
    target_template.maskParams={'sd':amplitude/2}


#C. Create a function for the gratings                                 Drifting gratings
#define some stuff
d_grating = 4
sf_grating = 1.4
pos_grating = np.array([[-5, 0], [5,0]])
GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 90, pos = pos_grating[0])
GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])


t_left_pos, t_right_pos = create_target_positions(size = 84)

for i in range(t_left_pos.shape[0]): 
    target_prepare(target_loc = 0, amplitude = 30, left_i = i, right_i = None)
    GratingA.draw()
    target_template.draw()
    win.flip()
    
    response = event.waitKeys(keyList = ['f', 'j', 'esc', 'escape'])
    if response[0] == 'f': 
        print('target located at: {}')
    elif response[0] == 'esc' or response[0] == 'escape': 
        break 
    else: 
        print('target NOT located at {}')





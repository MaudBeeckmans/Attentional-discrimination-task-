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
from Target_positions_function import create_target_positions


#B. Create the fixation point with function                                     Fixation point
#create the fixation point              #check whether the variables are important (maybe for formula)

win = visual.Window(size = [800, 600], monitor = 'Laptop', units = 'deg')



target_template =visual.GratingStim(win=win,tex='sin', mask='gauss',ori=90, sf=1.4, pos=(1,1), size= (1,1), interpolate=False, contrast = 1)
left_count = 0
right_count = 0
def target_prepare(target_loc = None, contrast = 1, opacity = 1, left_i = left_count, right_i = right_count):         #target location: '0.0' = L, '1.0' = R
                                                                                                        #corresponds with trial['Target_hemifield']
    if target_loc == 0: 
        target_position = t_left_pos[left_i, :]
    else: 
        target_position = t_right_pos[right_i, :]
    target_template.pos = target_position
    target_template.opacity = opacity
    target_template.contrast = contrast


#C. Create a function for the gratings                                 Drifting gratings
#define some stuff
d_grating = 4
sf_grating = 1.4
pos_grating = np.array([[-5, 0], [5,0]])
GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[0])
GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])

target2 = visual.GratingStim(win=win,tex='sin', mask='gauss',ori=0, sf=1.4, pos=(-4,0), size= (1,1), interpolate=False)
target3 = visual.GratingStim(win=win,tex='sin', mask='gauss',ori=0, sf=1.4, pos=(-6,0), size= (1,1), interpolate=False)

test_opa = 0.5
test_contr = 1
target2.opacity = test_opa


t_left_pos, t_right_pos = create_target_positions(size = 84)

for i in range(int(84/2)): 
    target_prepare(target_loc = 1, opacity = test_opa, contrast = test_contr, left_i = i, right_i = i)
    
    #target_template.pos = possible_loc[i]
    #target2.pos = t_left_pos[i+1]
    
    GratingA.draw()
    GratingB.draw()
    target_template.draw()
    win.flip()
#    for Frame in range(40): 
#        GratingA.draw()
#        GratingB.draw()
#        if Frame == 36 or Frame == 37: 
#            target_template.draw()
        #target2.draw()
    #    target2.draw()
    #    target3.draw()
        #win.flip()
    
    response = event.waitKeys(keyList = ['f', 'j', 'esc', 'escape'])
    if response[0] == 'f': 
        print('target located at: {}')
    elif response[0] == 'esc' or response[0] == 'escape': 
        break 
    else: 
        print('target NOT located at {}')


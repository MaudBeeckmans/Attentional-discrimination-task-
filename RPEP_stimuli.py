# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:42:38 2020

@author: Maud
"""

"""File that contains the creation of all the relevant stimuli, should be copied in both Experimental_file & 
Staircase_file"""

from psychopy import visual, data, event, core, gui
import os, pandas, math
import numpy as np




#A. Some general stuff                                                          General stuff 
#create window
def create_general_stimuli(win_size = 'fullscr', responseoptions = np.array(['f', 'j', 'esc', 'escape'])): 
    """Functions that creates the general stimuli at the beginning
    - creates: window (win), ResponseOptions"""
    global ResponseOptions, win
    if win_size == 'fullscr':     
        win = visual.Window(fullscr = True, units = "deg", monitor = "Laptop", mouseVisible = False)
    else: 
        win = visual.Window(size = win_size, units = "deg", monitor = "Laptop", mouseVisible = False)
    ResponseOptions = responseoptions
#%%
def create_fixation_point(): 
    """Functions that creates the basic stimuli for the fixation_point
    - created variables: dot_b, dot_s, line_h, line_v, line_d1, line_d2, d1, d2, r1, r2, ppd, point_d, Fixation_types"""
    global dot_b, dot_s, line_h, line_v, line_d1, line_d2, d1, d2, r1, r2, ppd, point_d, Fixation_types
    d1 = 0.6       #diameter outer circle (degrees)
    d2 = 0.2        #diameter inner circle (degrees)
    r1 = d1/2
    r2 = d2/2
    #calculate on site: https://www.sr-research.com/visual-angle-calculator/
    ppd = 45 #find formula to transpose pixels to visual degrees (here pixel per degree)
    point_d = math.sqrt(r1**2/2)
    dot_b = visual.Circle(win, color = 'black', radius = r1, fillColor = 'black', lineColor = 'Black', lineWidth = 0)
    dot_s = visual.Circle(win, color = 'black', radius = r2, fillColor = 'black', lineColor = 'Black', lineWidth = 0)
    line_v = visual.ShapeStim(win, vertices = ((0,-r1),(0,r1)), lineColor = 'white', 
                     fillColor = 'white', lineWidth  = ppd*d2)
    line_h = visual.ShapeStim(win, vertices = ((-r1,0),(r1, 0)), lineColor = 'white', 
                          fillColor = 'white', lineWidth = ppd*d2)
    line_d1 = visual.ShapeStim(win, vertices = ((-point_d, -point_d),(point_d, point_d)), 
                               lineColor = 'white', fillColor = 'white', lineWidth = ppd*d2)
    line_d2 = visual.ShapeStim(win, vertices = ((-point_d, point_d), (point_d, -point_d)), 
                               lineColor = 'white', fillColor = 'white', lineWidth = ppd*d2)
    Fixation_types = np.array(['plus', 'cross'])


def fixation_set_position(x = 0, y = 0, fix_type = 'plus'): 
    """Function to put the fixation_type at the correct position
    - only used inside the catch_trials functions I think"""
    dot_b.pos = (x, y)
    dot_s.pos = (x,y)
    if fix_type == 'plus': 
        line_v.vertices = ((0+x,-r1+y),(0+x,r1+y))
        line_h.vertices = ((-r1+x,0+y),(r1+x, 0+y))
    else: 
        line_d1.vertices = ((-point_d+x, -point_d+y),(point_d+x, point_d+y))
        line_d2.vertices = ((-point_d+x, point_d+y), (point_d+x, -point_d+y))

#fix_type = '' should be filled in with the type for that trial
def fixation_draw(fix_type = 'plus'):             #draws the fixation, does not flip it yet!
    """Function that draws the fixation_cross, based on its type"""
    if fix_type == 'plus': 
        dot_b.draw()
        line_h.draw()
        line_v.draw()
        dot_s.draw()
    else: 
        dot_b.draw()
        line_d1.draw()
        line_d2.draw()
        dot_s.draw()
#%%
def catch_trials_prepare(n_catchtrials = None, n_blocktrials = None, n_blocks = None): 
    """Function that allows for catch_trials
    - Creates catch_trials = array that contains (per row) the values for the catch_trials of each block
            (catch_trials.shape = n_blocks x n_catchtrials)
    - Creates catch_fix_positions: will be used in the catch_trial_execution function 
            (X-values for the positions of the fixations when catch_trial)
    - Creates FB_catch_wrong & FB_catch_correct: will be used in catch_trial_feedback() function"""
    global catch_trials, catch_question, catch_fix_positions, FB_catch_correct, FB_catch_wrong
    for i in range(n_blocks): 
        repeat = True
        while repeat == True: 
            catch_trials_block = np.random.randint(0, n_blocktrials, n_catchtrials)
            if np.unique(catch_trials_block).shape[0] == n_catchtrials: 
                repeat = False
        if i == 0: 
            catch_trials = catch_trials_block
        else: 
            catch_trials = np.row_stack([catch_trials, catch_trials_block])
    catch_question = visual.TextStim(win, text = str('Welk fixatiekruis heb je voor het laatst gezien: Het linker'
                                                 + ' of het rechter? \n Druk \'f\' als je links denkt,'
                                                 +'\'j\' als je rechts denkt'), pos = (0, 0.5), 
                                     wrapWidth = 1.9, units = 'norm')
    catch_fix_positions = np.array([-4, 4])
    #allow to display FB on the catch trial 
    FB_catch_correct = visual.TextStim(win, text = 'Juist')
    FB_catch_wrong = visual.TextStim(win, text = 'Fout, probeer tijdens de trial te fixeren op het fixatiekruis')
# catch_trials_prepare(n_catchtrials = 4, n_blocktrials = 84, n_blocks = 6)

def catch_trial_execution(): 
    """Function that executes the catch_trial
    - Draw the catch_question & fixation_types at correct positions
    - Store response of the pp (returns: catch_response)
    - Set fixation_positions back to 0, 0 after completion"""
    catch_question.draw()
    #draw the left fixation: plus
    for i, pos in enumerate(catch_fix_positions): 
        fixation_set_position(x = pos, y = 0, fix_type = Fixation_types[i])
        fixation_draw(fix_type = Fixation_types[i])
    win.flip()
    catch_response = event.waitKeys(keyList = ResponseOptions)
    for i in range(2): 
        fixation_set_position(x = 0, y = 0, fix_type = Fixation_types[i])
    return catch_response

def catch_trial_feedback(correct_button = 0, response = None): 
    """Function that draws feedback on the catch_trials, based on the catch_response from function 'catch_execution'.
    - Returns: accuracy (catch_accuracy)"""
    if response == correct_button: 
        FB_catch_correct.draw()
        accuracy = 1
        duration = 0.5
    else: 
        FB_catch_wrong.draw()
        accuracy = 0
        duration = 2 
    win.flip()
    core.wait(duration)
    return accuracy
    
#%%
#C. Create a function for the gratings                                          Gratings
def create_gratings(): 
    """Function that creates the 2 big gratings. 
    - created variables: d_grating, sf_grating, pos_grating, GratingA, GratingB"""
    global d_grating, sf_grating, pos_grating, GratingA, GratingB
    #define some stuff
    d_grating = 4
    sf_grating = 1.4
    pos_grating = np.array([[-5, 0], [5,0]])
    GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[0])
    GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])

def gratings_draw():
    """Fcuntion that draws the 2 gratings"""
    GratingA.draw()
    GratingB.draw()

#%%
#create a function to create arrays that contain the positions of the dots for both left & right flash 
def create_flashpos_arrays(): 
    """function that creates 2 arrays with the pos_values for 4 dots for both left & right flash: 
        - flash_left & flash_right: will be used in function flash_prepare()"""
    global flash_left, flash_right
    flash_positions = np.array([0, 1])      #0 = left, 1 = right 
    for i in range(flash_positions.shape[0]): 
        if flash_positions[i] == 0: 
            x_left = pos_grating[0,0] - d_grating/2 - 1.5
            x_right = pos_grating[0,0] + d_grating/2 + 1.5
            x_updown = pos_grating[0,0]
            y_leftright = pos_grating[0,1]
            y_up = pos_grating[0,1] + d_grating/2 + 1.5
            y_down = pos_grating[0,1] - d_grating/2 - 1.5
        else: 
            x_left = pos_grating[1,0] - d_grating/2 - 1.5
            x_right = pos_grating[1,0] + d_grating/2 + 1.5
            x_updown = pos_grating[1,0]
            y_leftright = pos_grating[1,1]
            y_up = pos_grating[0,1] + d_grating/2 + 1.5
            y_down = pos_grating[0,1] - d_grating/2 - 1.5
        dot_left = np.array([x_left, y_leftright])
        dot_right = np.array([x_right, y_leftright])
        dot_up = np.array([x_updown, y_up])
        dot_down = np.array([x_updown, y_down])
        if i == 0: 
            flash_left = np.array([dot_left, dot_right, dot_up, dot_down])
        else: 
            flash_right = np.array([dot_left, dot_right, dot_up, dot_down])
    
# flash_left, flash_right = create_flashpos_arrays()         #This is how to use the function "create_flashpos_arrays()"
#                                                             #(not !! to use this function anymore after this line)
def create_flash(): 
    """Funciton that creates the 4 dot_templates, !! to draw the flash"""
    global dot_template1, dot_template2, dot_template3, dot_template4
    dot_template1 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
    dot_template2 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
    dot_template3 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
    dot_template4 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
#create a function to display the flash 
def flash_prepare(position = 0):                  # in trialloop: "position = 'L'" should be replaced by "position = trial[flash_position]"
    """Function that adapts the positions of the dot_templates based on the flash_left & flash_right arrays: 
        - position = where the flash should appear"""
    if position == 0: 
        dot_template1.pos = flash_left[0]
        dot_template2.pos = flash_left[1]
        dot_template3.pos = flash_left[2]
        dot_template4.pos = flash_left[3]
    else: 
        dot_template1.pos = flash_right[0]
        dot_template2.pos = flash_right[1]
        dot_template3.pos = flash_right[2]
        dot_template4.pos = flash_right[3]

def flash_draw(): 
    """Function that draws the flash"""
    dot_template1.draw()
    dot_template2.draw()
    dot_template3.draw()
    dot_template4.draw()

#%%
# E. Create the Target  
def create_target(): 
    """Function that creates the target templates, left_count & right_count"""
    global target_template, left_count, right_count
    target_template =visual.GratingStim(win=win,tex='sin', mask='gauss',ori=90, sf=1.4, pos=(1,1), size= (1,1), 
                                        interpolate=False)
    left_count = 0
    right_count = 0

def create_target_positions(size = None, sf = 1.4): 
    """Function that creates the correct positions for target that appear on the left & right side of the screen 
    Input: size = the total amount of trials, sf = spatial frequency of the gratings, for same target visibility 
        every trial
    Created variables: target_left_positions, target_right_positions
       - will be used in function target_prepare"""
    global target_left_positions, target_right_positions
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

def target_prepare(target_loc = 0, opacity = 1, left_i = 0, right_i = 0):
    """Function that prepares the target for each trial."""
    if target_loc == 0: 
        target_position = target_left_positions[left_i, :]
    else: 
        target_position = target_right_positions[right_i, :]
    target_template.pos = target_position
    target_template.opacity = opacity

#%%
def create_extra_response_screen(time = 1000): 
    """Function that allows for extra response: 
        - created variables: extra_response_screen & extra_response_time (in ms)"""
    global extra_response_screen, extra_response_time
    extra_response_screen = visual.TextStim(win, text = 'Antwoord!')
    extra_response_time = time

#%%
def create_text_templates(euro_points = 600, trial_points = 10, FB_trial_dur = 0.5, FB_block_dur = 2): 
    """Function that creates the variables necessary to define the functions: 'message', 'FB_trial' & 'FB_block'
    - created variables: message_template, FB_template, FB_options, points_per_euro, points_per_trial, point_options, 
                        FB_block_duration, FB_trial_duration, total_points (0)
    - """
    global message_template, FB_template, FB_options, points_per_euro, points_per_trial, point_options
    global FB_block_duration, FB_trial_duration, total_points
    message_template = visual.TextStim(win, text = '')
    FB_template = visual.TextStim(win, text = '')
    FB_trial_duration = FB_trial_dur
    FB_options = np.array(['Fout', 'Juist', 'Te traag'])
    points_per_euro = euro_points
    points_per_trial = trial_points
    total_points = 0
    point_options = np.array(['+0', str('+' + str(points_per_trial)), '+0'])          #wrong, correct, no answer given 
    FB_block_duration = FB_block_dur
# create_text_templates()

def message(message_text = '', duration = 0, response_keys = ['space'], color = 'white', height = 0.1, 
            wrapWidth = 1.9, flip = True, position = (0,0), speedy = 0):
    space = "(Druk op spatie om verder te gaan.)"
    message_template.text = message_text + space
    message_template.pos = position
    message_template.units = "norm"
    message_template.color = color
    message_template.height = height 
    message_template.wrapWidth = wrapWidth 
    message_template.draw()
    if flip == True: 
        win.flip()
        if speedy == 1: 
            core.wait(0.01)
        else: 
            if duration == 0:
                #when duration = 0, wait till participant presses the right key (keys allowed can be found in response_keys, default allowed key is 'space')
                event.waitKeys(keyList = response_keys)
            else: 
                core.wait(duration)

def feedback_trial_experiment(block_type = 'REWARD', accuracy = 0, duration = 0, speedy = 0):        #accuracy should be matched based on acc. & block_type based on type
    if block_type == 'REWARD': 
        FB_text = str(FB_options[accuracy] + " " + point_options[accuracy])
    else: 
        FB_text = str(FB_options[accuracy] + " " + point_options[0])
    FB_template.text = FB_text
    FB_template.draw()
    win.flip()
    if speedy == 1: 
        core.wait(0.1)
    else: 
        core.wait(duration)

def feedback_trial_staircase(accuracy = 0, duration = 0):#accuracy should be matched based on acc.
    FB_text = str(FB_options[accuracy])
    FB_template.text = FB_text
    FB_template.draw()
    win.flip()
    core.wait(duration)

def feedback_block(durationR = 0, block_type = 'REWARD', blockP = 0, totalP = 0, speedy = 0):
    if block_type == 'REWARD': 
        FB_block_text = "Einde van dit blok. \nPunten dit blok = {0} \n Punten totaal = {1} ".format(blockP, totalP)
        duration = durationR
    else: 
        FB_block_text = "Einde van dit blok." 
        duration = 1
    FB_template.text = FB_block_text 
    FB_template.draw()
    win.flip()
    if speedy == 1: 
        core.wait(0.1)
    else: 
        core.wait(duration)

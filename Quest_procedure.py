# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 16:01:59 2020

@author: Maud
"""

from psychopy import visual, data, event, core, gui
import os, pandas, math
import numpy as np
from RPEP_functions import create_output_file, create_design_fixed, create_design_complete, create_pandas_design
from RPEP_functions import create_target_positions

#%%
#Create the correct map & ExperimentHandler: with info, output_file
my_home_directory, my_output_directory, pp_number, name, thisExp = create_output_file(map_name = 'Output_staircase', 
                                                                                      file_name = 'Stairfile_pp')
#%%Define the speedy & try_out
speedy = 0
try_out = 1
fullscreen = True

#%%create the design
n_blocks = 1
framerate = 1000/60
#Create the basic design (FTI x Flash position x Target relative position)
Fixed_blocks, n_blocktrials, n_trials = create_design_fixed(n_blocks = n_blocks)
#Create the complete array (not stored anywhere yet)

Design_array, Fixation_options = create_design_complete(n_blocks = n_blocks, Basic_array = Fixed_blocks, 
                                                                n_blocktrials = n_blocktrials, n_trials = n_trials)

#Create the dataframe with pandas
Design_DF= create_pandas_design(array = Design_array, used_map = my_output_directory, 
                                                   number = pp_number)
# Index(['TrialN', 'BlockN', 'BlocktrialN', 'FTI', 'Flash_position',
#        'Target_relative_position', 'CorResp', 'Target_hemifield',
#        'Grating_start', 'Grating_Flash', 'Flash_start', 'Target_start',
#        'MaxFrames', 'Fixation_type_bin'],
#       dtype='object')

#%%create stiimuli & variables that should be created before the loops
#Create window & ResponseOptions
if fullscreen == True: 
    win = visual.Window(fullscr = True, units = 'deg', monitor = 'Laptop', mouseVisible = False)
else: 
    win = visual.Window(size = [800, 600], units = "deg", monitor = "Laptop", mouseVisible = False)
ResponseOptions = np.array(['f', 'j', 'esc', 'escape'])
flash_frames = 2
target_frames = 2

#Create the fixation point 
d1 = 0.6       #diameter outer circle (degrees)
d2 = 0.2        #diameter inner circle (degrees)
r1 = d1/2
r2 = d2/2
#calculate on site: https://www.sr-research.com/visual-angle-calculator/
ppd = 45 #find formula to transpose pixels to visual degrees (here pixel per degree)
ppd = 30
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

#Create the stimuli for the catch_trials
n_catchtrials = int(n_blocktrials / 20)
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

#Create the gratings & !! variables 
d_grating = 4
sf_grating = 1.4
pos_grating = np.array([[-5, 0], [5,0]])
GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[0])
GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])

#Create the flash
dot_template1 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
dot_template2 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
dot_template3 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
dot_template4 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')

#Create the stimuli & variables for the target
target_template =visual.GratingStim(win=win,tex='sin', mask='gauss',ori=90, sf=1.4, pos=(1,1), size= (1,1), 
                                        interpolate=False)
left_count = 0
right_count = 0

#Create stimuli for the extra_response_screen
extra_response_screen = visual.TextStim(win, text = 'Antwoord!')
extra_response_time = 1000

#Create the stimuli & variables for the messages & FB
message_template = visual.TextStim(win, text = '')
FB_template = visual.TextStim(win, text = '')
FB_trial_duration = 0.5
FB_options = np.array(['Fout', 'Juist', 'Neutraal', 'Te traag'])

#Stimuli necessary for the instructions
greeting = 'Hallo ' + name
spatie = '\n\n(Druk op spatie om verder te gaan)'
InstructionsP0 = str('Instructies: In deze taak zal je de locatie van een target (links of rechts) aangeven. '
                     +'De target verschijnt steeds in 1 van 2 gepresenteerde gratings (links & rechts). '
                     + 'De taak wordt in meer detail uitgelegd op volgende pagina\'s. ' + spatie)
InstructionsP1 = str('\nElke trial zal beginnen met een fixatiekruis. Hiernaast zullen 2  '
                     + 'gratings verschijnen. Probeer je aandacht naar deze 2 gratings te richten, maar kijk ' 
                     + 'vooral steeds naar het fixatiekruis. Probeer dus geen oogbewegingen te maken.'
                     + spatie)
InstructionsP2 = str('Het doel is de detectie van een target in één van de 2 gratings. De target verschijnt '
                     + 'maar voor een heel korte periode. Er is telkens evenveel kans ' 
                     + 'dat de target in de ene als de andere grating verschijnt. Geef aan in welke grating de ' 
                     + 'target verscheen met de toetsen f en j: \n\'f\' = LINKS      \'j\' = RECHTS.'
                     + '\nDoe dit zo ACCURAAT mogelijk.' + spatie)
InstructionsP3 = str('Geef ALTIJD een antwoord, ook als je de target niet hebt gezien. Antwoorden is mogelijk '
                     + 'vanaf de target is verschenen. Wanneer \'Antwoord!\' op het scherm verschijnt is je '
                     + 'tijd om te antwoorden bijna om. Geef dan zo snel mogelijk een antwoord.'
                     + spatie)
InstructionsP4 = str('Korte samenvatting van de belangrijkste zaken: '
                     + '\n     - Kijk steeds naar het fixatiekruis'
                     + '\n     - Target altijd 50% kans om L als R te verschijnen'
                     + '\n     - Antwoordopties: links = \'f\', rechts = \'j\''
                     + '\n     - Geef ELKE TRIAL een antwoord'
                     + spatie)
InstructionsP5 = str('Moest je nog vragen hebben, kom dan gerust eens kloppen bij de proefleider. Deze helpt '
                     +'je zeer graag verder. Als je geen vragen meer hebt, gelieve dan je hoofd op de '
                     + 'hoofdsteun te leggen en vergeet niet steeds naar het fixatiekruis te kijken. Succes.' 
                     + spatie)

instructions_text = visual.TextStim(win, height = 0.1, units = 'norm', wrapWidth = 1.9, pos = (0, 0.5), alignText = 'left')
instructions_image = visual.ImageStim(win, image = None, pos = (0, -0.5), units = 'norm', size = (1.9, 1))
path = my_home_directory

#%%Create the functions to manipulate the stimuli

#Functions to manipulate the fixation cross
def fixation_set_position(x = 0, y = 0, fix_type = 'plus'): 
    """Function to put the fixation_type at the correct position
    - only used inside the catch_trials functions I think
    - run once before loops as well to make sure the fixation crosses have the correct position"""
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

#Functions to manipulate the catch trials 
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

def catch_trial_feedback(correct_button = 0, response = None, speedy = 0): 
    """Function that draws feedback on the catch_trials, based on the catch_response from function 'catch_execution'.
    - Returns: accuracy (catch_accuracy)"""
    if response == correct_button: 
        FB_catch_correct.draw()
        accuracy = 1
        if speedy == 0: 
            duration = 0.5
        else: 
            duration = 0
    else: 
        FB_catch_wrong.draw()
        accuracy = 0
        if speedy == 0: 
            duration = 2 
        else: 
            duration = 0
    win.flip()
    core.wait(duration)
    return accuracy

#Functions to manipulate the gratings
def gratings_draw():
    """Fcuntion that draws the 2 gratings"""
    GratingA.draw()
    GratingB.draw()

#Functions to manipulate the flash 
def create_flashpos_arrays(): 
    """function that creates 2 arrays with the pos_values for 4 dots for both left & right flash: 
        - flash_left & flash_right: will be used in function flash_prepare()"""
    flash_positions = np.array([0, 1])      #0 = left, 1 = right 
    for i in flash_positions: 
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
    return flash_left, flash_right

def flash_prepare(position = 0): # in trialloop: "position = 0" should be replaced by "position = trial[flash_position]"
    """Function that adapts the positions of the dot_templates based on the flash_left & flash_right arrays: 
        - position = where the flash should appear
        - run 'create_flashpos_arrays' once before running this function"""
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

#Functions to manipulate the target
def target_prepare(target_loc = 0, opacity = 1, left_i = 0, right_i = 0):
    """Function that prepares the target for each trial.
    - run 'create_target_positions' function before you run this function!"""
    if target_loc == 0: 
        target_position = target_left_positions[left_i, :]
    else: 
        target_position = target_right_positions[right_i, :]
    target_template.pos = target_position
    target_template.opacity = opacity

#Function to display text
def message(message_text = '', duration = 0, response_keys = ['space'], color = 'white', height = 0.1, 
            wrapWidth = 1.9, flip = True, position = (0,0), speedy = 0):
    message_template.text = message_text
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

#Functions to display feedback 
def feedback_trial_staircase(accuracy = 0, duration = 0):#accuracy should be matched based on acc.
    FB_text = str(FB_options[accuracy])
    FB_template.text = FB_text
    FB_template.draw()
    win.flip()
    core.wait(duration)

#Function to display instructions
def instructions_stair(page = 1): 
    if page == 0: 
        instructions_text.text = InstructionsP0
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 1: 
        instructions_text.text = InstructionsP1
        instructions_text.pos = (0, 0.5)
        instructions_image.image = path + "\Instructies_Exp1.png"
    elif page == 2: 
        instructions_text.text = InstructionsP2
        instructions_text.pos = (0, 0.5)
        instructions_image.image = path + "\Instructies_Exp3.png"
    elif page == 3: 
        instructions_text.text = InstructionsP3
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 4: 
        instructions_text.text = InstructionsP4
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 5: 
        instructions_text.text = InstructionsP5
        instructions_image.image = None
    instructions_text.draw()
    instructions_image.draw()
    win.flip()
    event.waitKeys(keyList = 'space')

#%%
flash_left, flash_right = create_flashpos_arrays()
response_frames = int(np.round(1000/framerate, 0))
clock = core.Clock()
check_clock = core.Clock()

#%%The train_trials
n_traintrials = 6
target_left_positions, target_right_positions = create_target_positions(size = n_traintrials, sf = 1.4)


message(message_text = greeting, duration = 1, speedy = speedy)
if speedy == 0: 
    for i in range(0, 6):
        instructions_stair(page = i)


#%%Create QuestHandler
#startval: 0.25; startValSd = 0.15
staircase1 = data.QuestHandler(startVal = 0.25, startValSd = 0.15, nTrials = n_trials/2, pTreshold = 0.70)
staircase2 = data.QuestHandler(startVal = 0.25, startValSd = 0.15, nTrials = n_trials/2, pTreshold = 0.70)

left_count = 0
right_count= 0
#%%The staircase itself
target_left_positions, target_right_positions = create_target_positions(size = n_trials, sf = 1.4)
DesignTL = pandas.DataFrame.to_dict(Design_DF, orient = "records")
trials = data.TrialHandler(trialList = DesignTL, nReps = 1, method = "sequential")
thisExp.addLoop(trials)

message(message_text = 'Vanaf nu is het voor echt.' + spatie)
for trial in trials: 
    response = None
    response_RT = None
    if trial['Target_hemifield'] == 0: 
        this_opacity = staircase1._nextIntensity
        trials.addData('Opacity_left', this_opacity)
    else: 
        this_opacity = staircase2._nextIntensity
        trials.addData('Opacity_right', this_opacity)
    target_prepare(target_loc = trial['Target_hemifield'], opacity = this_opacity, left_i = left_count, 
                   right_i = right_count)
    fix_type_trial = Fixation_types[trial['Fixation_type_bin']]
    
    #Define the timings
    t0 = 45 #Base on this startframe + the FTI the frame on which the target appears is defined
            #first frame where target can appear = 30 (is the same as in real experiment)
    start_grating = trial['Grating_start']
    start_target = start_grating + t0 + trial['FTI']
    stop_target = start_target + target_frames
    max_frames = start_target + response_frames
    
    if trial['BlocktrialN'] in catch_trials: 
        if speedy == 0: 
            for Frame in range(60):     
                fixation_draw(fix_type = fix_type_trial)
                if Frame > 33: 
                    gratings_draw()
                win.flip()
            catch_response = catch_trial_execution()
        else: 
            catch_response = np.array(['f'])
        catch_accuracy = catch_trial_feedback(correct_button = ResponseOptions[trial['Fixation_type_bin']], 
                                              response = catch_response[0], speedy = speedy)
    
    for frame in range(max_frames): 
        fixation_draw(fix_type = fix_type_trial)
        if frame >= start_grating: 
            gratings_draw()
        if frame >= start_target and frame < stop_target: 
            target_template.draw()
        win.flip()
        if frame == start_target: 
            clock.reset()
            event.clearEvents(eventType = 'keyboard')
        if frame >= start_target: 
            response = event.getKeys(keyList = ResponseOptions, timeStamped = clock)
            response = np.array(response).squeeze()
            if speedy == 1 and frame >= stop_target: 
                response = np.array(['f', 0])
            if len(response) != 0:
                break 
    #allow for extra response time if no response has been given yet 
    if len(response) == 0: 
        extra_response_screen.draw()
        win.flip()
        response = event.waitKeys(keyList = ResponseOptions, maxWait = extra_response_time/1000, timeStamped = clock)
        response = np.array(response).squeeze()
        if np.all(response == None): 
            response = np.array([-1, -1])
            trial_accuracy, stair_accuracy = -1, 0 #for staircase make the accuracy 0 instead of -1 
                #has to be -1 for the correct feedback
        extra_time = True
    else: 
        extra_time = False
    
    #define the accuracy 
    CorResp = ResponseOptions[trial['CorResp']]
    if np.all(response[0] == 'esc') or np.all(response[0] == 'escape'): 
        break
    elif np.all(CorResp == response[0]): 
        trial_accuracy, stair_accuracy = 1, 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy, stair_accuracy = 0, 0
    
    if speedy == 0: 
        if try_out == 0: 
            feedback_trial_staircase(accuracy = trial_accuracy, duration = FB_trial_duration)
        else: 
            feedback_trial_staircase(accuracy = 2, duration = FB_trial_duration)
    #Adapt the staircase values
    if trial['Target_hemifield'] == 0: 
        #hier de staircase aanpassen 
        left_count = left_count + 1
        staircase1.addResponse(stair_accuracy)
    else: 
        #hier de staircase aanpassen 
        right_count = right_count + 1
        staircase2.addResponse(stair_accuracy)
    
    trials.addData('Response', response[0])
    trials.addData('RT', response[1])
    trials.addData('Accuracy', trial_accuracy)
    
    if trial['BlocktrialN'] == n_blocktrials: 
        trials.addData('QuantileL', np.round(staircase1.quantile(), 2))
        trials.addData('QuantileR', np.round(staircase2.quantile(), 2))
        trials.addData('MeanL', np.round(staircase1.mean(), 2))
        trials.addData('MeanR', np.round(staircase2.mean(), 2))
        trials.addData('ModeL', np.round(staircase1.mode(), 2))
        trials.addData('ModeR', np.rond(staircase1.mode(), 2))
    thisExp.nextEntry()

message('Het eerste deel is gedaan, gelieve even bij de proefleider te gaan kloppen.')

win.close()

stored_opa = np.array([np.round(staircase1.quantile(0.3), 2), np.round(staircase2.quantile(0.3), 2)])
opacity_file = my_output_directory + '/Stair_opacity' + str(pp_number)
np.save(opacity_file + '.npy', stored_opa)

print(staircase1.mean(), staircase2.mean())
print(staircase1.quantile(0.3), staircase2.quantile(0.3))
print(staircase1.mode(), staircase2.mode())





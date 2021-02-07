# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 15:03:24 2020

@author: Maud
"""

from psychopy import visual, data, event, core, gui
import os, pandas, math
import numpy as np
from RPEP_functions import create_output_file, create_design_fixed, create_design_complete, create_pandas_design
from RPEP_functions import create_target_positions


#%%
#Create the correct map & ExperimentHandler: with info, output_file
my_home_directory, my_output_directory, pp_number, name, thisExp = create_output_file(map_name = 'Output_experiment', 
                                                                                      file_name = 'Outputfile_pp')
#%%Define the speedy & try_out
speedy = 0
try_out = 1
fullscreen = True
try_out_opa = 0.3758

#%%create the design
n_blocks = 6
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
catch_question = visual.TextStim(win, text = str('Is dit fixatiekruis is HETZELFDE als hetgeen je net hebt gezien.'
                            +'\n Druk \'f\' voor ja, \'j\' voor nee.'), pos = (0, 0.5), 
                            wrapWidth = 1.9, units = 'norm')

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
FB_options = np.array(['Fout', 'Juist', 'Te traag'])
points_per_euro = 600
points_per_trial = 10
total_points = 0
point_options = np.array(['+0', str('+' + str(points_per_trial)), '+0'])          #wrong, correct, no answer given 
FB_block_duration = 2

#Stimuli !! for the instructions 
#The instructions (in Dutch)
spatie = '\n\n(Druk op spatie om verder te gaan)'
greeting = "Hallo " + name 
InstructionsP0 = str('Instructies: Het doel van de taak zal zijn een target te detecteren in 1 van 2 gepresenteerde '
                     +'gratings. De taak wordt in meer detail uitgelegd op volgende pagina\'s.' + spatie)
InstructionsP1 = str('\nElke trial zal beginnen met een fixatiekruis. Hiernaast zullen 2  '
                     + 'gratings verschijnen. Probeer je aandacht naar deze 2 gratings te richten, maar kijk ' 
                     + 'vooral steeds naar het fixatiekruis. Probeer dus geen oogbewegingen te maken.'
                     + spatie)
InstructionsP2 = str('Tijdens elke trial zal een flash rond één van de gratings verschijnen. Deze is totaal ' 
                     'IRRELEVANT voor de taak, probeer deze dus zo goed mogelijk te negeren.' + spatie)
InstructionsP3 = str('Het doel is de detectie van een target in één van de 2 gratings. Er is telkens evenveel kans ' 
                     + 'dat de target in de ene als de andere grating verschijnt. Geef aan in welke grating de ' 
                     + 'target verscheen met de toetsen f en j: \n\'f\' = LINKS      \'j\' = RECHTS.'
                     + '\nDoe dit zo ACCURAAT mogelijk.' + spatie)
InstructionsP4 = str('Geef ALTIJD een antwoord, ook als je de target niet hebt gezien. Antwoorden is mogelijk '
                     + 'vanaf de target is verschenen. Wanneer \'Antwoord!\' op het scherm verschijnt is je '
                     + 'tijd om te antwoorden bijna om. Geef dan zo snel mogelijk een antwoord.'
                     + spatie)
InstructionsP5 = str('Je zal zowel REWARD als NON REWARD blokken maken. In de REWARD blokken kan je punten verdienen:'
                     + '{} punten per correct antwoord. Per {} punten win je 1 EUR.'.format(points_per_trial, points_per_euro)
                     + 'In de NON REWARD blokken kan je geen punten verdienen. Aan het begin van elk blok wordt '
                     + 'het type blok aangegeven.' + spatie)
InstructionsP6 = str('Korte samenvatting van de belangrijkste zaken: '
                     + '\n     - Kijk steeds naar het fixatiekruis'
                     + '\n     - Negeer de flash'
                     + '\n     - Target altijd 50% kans om L als R te verschijnen'
                     + '\n     - Antwoordopties: links = \'f\', rechts = \'j\''
                     + '\n     - Geef ELKE TRIAL een antwoord'
                     + '\n     - REWARD blok: correct = punten (geld) verdienen'
                     + spatie)
InstructionsP7 = str('Moest je nog vragen hebben, kom dan gerust eens kloppen bij de proefleider. Deze helpt '
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
    #randomly select whether the cross or the plus is drawn 
    catch_cross = np.random.randint(0, 2, 1)
    fixation_draw(fix_type = Fixation_types[catch_cross])
    win.flip()
    catch_response = event.waitKeys(keyList = ResponseOptions)
    return catch_response, catch_cross

def catch_trial_feedback(correct_button = None, response = None, speedy = 0): 
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

#Display the instructions
def instructions(page = 1): 
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
        instructions_image.image = path + "\Instructies_Exp2.png"
    elif page == 3: 
        instructions_text.text = InstructionsP3
        instructions_text.pos = (0, 0.5)
        instructions_image.image = path + "\Instructies_Exp3.png"
    elif page == 4: 
        instructions_text.text = InstructionsP4
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 5: 
        instructions_text.text = InstructionsP5
        instructions_image.image = None
    elif page == 6: 
        instructions_text.text = InstructionsP6
        instructions_image.image = None
    elif page == 7: 
        instructions_text.text = InstructionsP7
        instructions_image.image = None
    instructions_text.draw()
    instructions_image.draw()
    win.flip()
    event.waitKeys(keyList = 'space')


#%%Create the stuff that still has to be created before the actual experimental loop 
#create the clocks
clock = core.Clock()
clock_check = core.Clock()

flash_left, flash_right = create_flashpos_arrays()
target_left_positions, target_right_positions = create_target_positions(size = n_trials, sf = 1.4)

#Create the sequence of the blocks (counterbalanced over pp.)
block_sequence = np.array([['REWARD', 'NON REWARD'], ['NON REWARD', 'REWARD']])
block_type_array = np.tile(block_sequence[pp_number%2], int(n_blocks/2))

#load the correct stair_opacity from the corresponding file for this pp in the staircase_output
if try_out == 0: 
    load_directory = 'C:\\Users\\Maud\\Documents\\Psychologie\\1ste_master_psychologie\\RPEP\\Experiment\\Eindproduct\\Output_stairCase'
    stair_opacityL = np.load(load_directory + '\Stair_opacity' + str(pp_number) + '.npy')
    stair_opacityR = stair_opacityL
#    stair_opacityL -= 0.05
#    stair_opacityR -= 0.05
else: 
    stair_opacityL, stair_opacityR = try_out_opa, try_out_opa


#%%
DesignTL = pandas.DataFrame.to_dict(Design_DF, orient = "records")
trials = data.TrialHandler(trialList = DesignTL, nReps = 1, method = "sequential")
thisExp.addLoop(trials)

#%% The actual experiment

message(message_text = greeting, speedy = speedy, duration = 1)
if speedy == 0: 
    for i in range(0, 8): 
        instructions(page = i)
for trial in trials: 
    response = None
    response_RT = None
    #define the correct opacity based on target in L or R hemifield
    if trial['Target_hemifield'] == 0: 
        this_opacity = stair_opacityL
    else: 
        this_opacity = stair_opacityR
    trials.addData('Target_opacity', this_opacity)
    #Prepare the flash & target positioning & opacity of target
    flash_prepare(position = trial['Flash_position'])
    target_prepare(target_loc = trial['Target_hemifield'], opacity = this_opacity, left_i = left_count, 
                   right_i = right_count)
    #define some variables
    fix_type_trial = Fixation_types[trial['Fixation_type_bin']]
    
    if trial['BlocktrialN'] == 0: 
        points_this_block = 0
        this_block_type = block_type_array[trial['BlockN']]
        message(message_text = str("Dit is blok {0}. Dit is een {1} blok.".format(trial['BlockN'] + 1, this_block_type) 
                                   + "\n Druk \'spatie\' om te starten."), speedy = speedy)
#2 lines below to test the catch_trials
#    catch_trials = np.random.randint(0, 10, 5)
#    if trial['BlocktrialN'] in catch_trials:
    if trial['BlocktrialN'] in catch_trials[trial['BlockN']]:
        if speedy == 0: 
            for Frame in range(60):     
                fixation_draw(fix_type = fix_type_trial)
                if Frame > 33: 
                    gratings_draw()
                win.flip()
            catch_response, catch_cross = catch_trial_execution()
        else: 
            catch_response = np.array(['f'])
            catch_cross = 1 #added
        CorResp_catch = (trial['Fixation_type_bin'] != catch_cross)*1      #if fix_type_trial == fix_type_catch, correct answer is 'f' (0)
        #print('0 / 1 for catch trial is {}'.format(CorResp_catch))
        catch_accuracy = catch_trial_feedback(correct_button = ResponseOptions[int(CorResp_catch)], 
                                          response = catch_response[0], speedy = speedy)
        print('Catch accuracy is {}'.format(catch_accuracy))
        trials.addData('Catch_accuracy', catch_accuracy)
    
    #make sure the frame loop duration is as short as possible
    max_frames = trial['MaxFrames']
    start_grating = trial['Grating_start']
    start_flash = trial['Flash_start']
    stop_flash = trial['Flash_start'] + flash_frames
    start_target = trial['Target_start'] 
    stop_target = trial['Target_start'] + target_frames
    
    
    #start the display of the frames for this trial
    win.recordFrameIntervals = True
    win.refreshThreshold = 1/framerate + 0.004
    clock_check.reset()
    for frame in range(max_frames): 
        fixation_draw(fix_type = fix_type_trial)
        if frame >= start_grating: 
            gratings_draw()
        if frame >= start_flash and frame < stop_flash: 
            flash_draw()
        if frame >= start_target and frame < stop_target: 
            target_template.draw()
        win.flip()
        if frame == start_target: 
            clock.reset()
            event.clearEvents(eventType = 'keyboard')
        
        if frame == start_grating: 
            Gr_appearT = clock_check.getTime()
        elif frame == start_flash: 
            Fl_appearT = clock_check.getTime()
        elif frame == stop_flash: 
            Fl_stopT = clock_check.getTime()
        
        if frame == start_target: 
            T_appearT = clock_check.getTime()
        elif frame == stop_target: 
            T_stopT = clock_check.getTime()
        
        if frame >= start_target: 
            response = event.getKeys(keyList = ResponseOptions, timeStamped = clock)
            response = np.array(response).squeeze()
            if speedy == 1 and frame >= stop_flash and frame >= stop_target: 
                response = np.array(['f', 0])
            if len(response) != 0:
                break 
    total_frames_dropped = win.nDroppedFrames
    win.recordFrameIntervals = False
    if len(response) == 0:
        extra_response_screen.draw()
        win.flip()
        response = event.waitKeys(keyList = ResponseOptions, maxWait = extra_response_time/1000, timeStamped = clock)
        response = np.array(response).squeeze()
        if np.all(response == None): 
            response = np.array([-1, -1])
            trial_accuracy = -1
        extra_time = True
    else: 
        extra_time = False  
    if np.all(response[0] == 'esc') or np.all(response[0] == 'escape'): 
        break
    elif np.all(ResponseOptions[trial['CorResp']] == response[0]): 
        trial_accuracy = 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy = 0
    
    feedback_trial_experiment(accuracy = trial_accuracy, block_type = this_block_type, duration = FB_trial_duration, 
                              speedy = speedy)
    if this_block_type == 'REWARD' and trial_accuracy == 1: 
        points_this_block = points_this_block + points_per_trial
        total_points = total_points + points_per_trial
    
    
    trials.addData('Response', response[0])
    trials.addData('Accuracy', trial_accuracy)
    trials.addData('RT', response[1])
    trials.addData('Extra_time_needed', extra_time)
    trials.addData('Total_points', total_points)
    trials.addData('Block_points', points_this_block)
    trials.addData('Gr_appear_T', Gr_appearT)
    trials.addData('Fl_appear_T', Fl_appearT)
    trials.addData('Fl_stop_T', Fl_stopT)
    trials.addData('T_appear_T', T_appearT)
    trials.addData('T_stop_T', T_stopT)
    trials.addData('Total_Dropped_Frames', total_frames_dropped)
    #allow to store the next entry 
    thisExp.nextEntry()
    
    if trial['Target_hemifield'] == 0: 
            left_count = left_count + 1
    else: 
        right_count = right_count + 1
    
    if np.all(response[0] == 'esc') or np.all(response[0] == 'escape'): 
        break
    
    if trial['BlocktrialN'] == n_blocktrials-1: 
        feedback_block(durationR = FB_block_duration, block_type = this_block_type, blockP = points_this_block, 
                       totalP = total_points, speedy = speedy)


message(message_text = 'Bedankt voor je deelname!')
win.close()

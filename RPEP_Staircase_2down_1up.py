# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 18:17:21 2021

@author: Maud
"""

"""info about this staircase: 2 down 1 up 
    - will use random intervals between grating appearance & target appearance 
    - will NOT use a flash 
"""

from psychopy import visual, data, event, core, gui
import os, pandas, math, pylab
import numpy as np
from RPEP_functions import create_target_positions, create_output_file

#Create the correct map & ExperimentHandler: with info, output_file
my_home_directory, my_output_directory, pp_number, name, thisExp = create_output_file(map_name = 'Output_staircase', 
                                                                                      file_name = 'Stairfile_pp', exp_type = 'staircase')
#to easily adapt
n_stair_trials = 60


#%%Define the speedy & try_out
speedy = 0
try_out = 0         #change to set the train_trials at 0
fullscreen = True
used_monitor = 'ExpMonitor'
#used_monitor = 'Laptop'

#calculate on site: https://www.sr-research.com/visual-angle-calculator/
#ppd = 50 #find formula to transpose pixels to visual degrees (here pixel per degree)
ppd = 30

#create the design
if try_out == 1: 
    n_train_trials = 0
else: 
    n_train_trials = 6
max_trials = n_stair_trials + n_train_trials
framerate = 1000/60         #time for 1 frame in ms (16,6666668)
Response_time_ms = 1000
Grating_start_limits_ms = np.array([500, 600+framerate])        #+framerate since the upper boundary isn't included
Grating_target_limits_ms = np.array([500, 2000 + framerate])
target_frames = 2         #Moet achteraf nog bepaald worden!!!!
Grating_start_limits = np.round(Grating_start_limits_ms/framerate, 0)
Grating_start_limits.astype(int)
Grating_target_limits = np.round(Grating_target_limits_ms/framerate, 0)
Grating_target_limits.astype(int)
#Create the arrays that contain the important timings & values for each trial (random)
Grating_start_array = np.random.randint(Grating_start_limits[0], Grating_start_limits[1], max_trials)
Grating_target_array = np.random.randint(Grating_target_limits[0], Grating_target_limits[1], max_trials)
Target_start_array = Grating_start_array + Grating_target_array

Fixation_types = np.array(['plus', 'cross'])
Fixation_type_array = np.concatenate([np.zeros(int(max_trials/2)), np.ones(int(max_trials/2))]).reshape(max_trials, 1)
np.random.shuffle(Fixation_type_array)
            #0 = plus, 1 = cross
#define target position and correct response
Target_pos = np.random.randint(0, 2, max_trials)
Cor_resp = np.copy(Target_pos)

Design_array = np.column_stack([Target_pos, Cor_resp, Grating_start_array, Target_start_array, Fixation_type_array])

#%%create stiimuli & variables that should be created before the loops
#Create window & ResponseOptions
if fullscreen == True: 
    win = visual.Window(fullscr = True, units = 'deg', monitor = used_monitor, mouseVisible = False)
else: 
    win = visual.Window(size = [800, 600], units = "deg", monitor = used_monitor, mouseVisible = False)
ResponseOptions = np.array(['f', 'j', 'esc', 'escape'])

#Create the fixation point 
d1 = 0.6       #diameter outer circle (degrees)
d2 = 0.2        #diameter inner circle (degrees)
r1 = d1/2
r2 = d2/2

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
n_catchtrials = int(max_trials / 20)
n_blocks = 1
for i in range(n_blocks): 
    repeat = True
    while repeat == True: 
        catch_trials_block = np.random.randint(n_train_trials, max_trials, n_catchtrials)
        if np.unique(catch_trials_block).shape[0] == n_catchtrials: 
            repeat = False
    if i == 0: 
        catch_trials = catch_trials_block
    else: 
        catch_trials = np.row_stack([catch_trials, catch_trials_block])
catch_question = visual.TextStim(win, text = str('Is dit fixatiekruis is HETZELFDE als hetgeen je net hebt gezien.'
                            +'\n Druk \'f\' voor ja, \'j\' voor nee.'), pos = (0, 0.5), 
                            wrapWidth = 1.9, units = 'norm')
#catch_fix_positions = np.array([-4, 4])

# line below is to test wheter the adapted catch trials are better (think they are): is the fix cross the same as the one you just saw? 
#catch_trials = np.array([1, 2, 3, 4])

#allow to display FB on the catch trial 
FB_catch_correct = visual.TextStim(win, text = 'Juist')
FB_catch_wrong = visual.TextStim(win, text = 'Fout, probeer tijdens de trial te fixeren op het fixatiekruis')

#Create the gratings & !! variables 
d_grating = 4
sf_grating = 1.4
pos_grating = np.array([[-5, 0], [5,0]])
GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[0])
GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])

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

instructions_text = visual.TextStim(win, height = 0.1, units = 'norm', wrapWidth = 1.9, pos = (0, 0.5))
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
#    for i, pos in enumerate(catch_fix_positions): 
#        fixation_set_position(x = pos, y = 0, fix_type = Fixation_types[i])
#        fixation_draw(fix_type = Fixation_types[i])
    win.flip()
    catch_response = event.waitKeys(keyList = ResponseOptions)
#    for i in range(2): 
#        fixation_set_position(x = 0, y = 0, fix_type = Fixation_types[i])
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
target_left_positions, target_right_positions = create_target_positions(size = max_trials*2, sf = 1.4)  #*2 since it doesn't have to be 50/50 left/right
store_opa = []
store_acc = []
response_frames = int(np.round(Response_time_ms/framerate, 0))
clock = core.Clock()
check_clock = core.Clock()


start_opa = 0.3
train_opa = 0.5

message(message_text = greeting, duration = 1, speedy = speedy)
if speedy == 0 and try_out == 0: 
    for i in range(0, 6):
        instructions_stair(page = i)

staircase = data.StairHandler(startVal=start_opa, stepType='lin',
    stepSizes=[0.02, 0.02, 0.01],  # reduce step size every two reversals
    minVal=0, maxVal=0.7,
    nUp=1, nDown=2,  # will home in on the 70% threshold
    nTrials=n_stair_trials)

message(message_text = 'Dit is een oefen-deel' + spatie)
this_trial = 0
for trial in range(n_train_trials): 
    this_opacity = train_opa
    #print(this_opacity)
    target_prepare(target_loc = Target_pos[this_trial], opacity = this_opacity, left_i = left_count, right_i = right_count)
    fix_type_trial = Fixation_types[int(Fixation_type_array[this_trial])]
    start_grating = Grating_start_array[this_trial]
    start_target = Target_start_array[this_trial]
    stop_target = start_target + target_frames
    max_frames = start_target + response_frames
    
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
    CorResp = ResponseOptions[int(Cor_resp[this_trial])]
    if np.all(response[0] == 'esc') or np.all(response[0] == 'escape'): 
        break
    elif np.all(CorResp == response[0]): 
        trial_accuracy, stair_accuracy = 1, 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy, stair_accuracy = 0, 0

    if Target_pos[this_trial] == 0:                        #these fucntions to adapt the position of the target inside the grating 
        left_count = left_count + 1
    else: 
        right_count = right_count + 1
    #print(stair_accuracy)
    
    if speedy == 0: 
        if try_out == 0: 
            feedback_trial_staircase(accuracy = trial_accuracy, duration = FB_trial_duration)
        else: 
            feedback_trial_staircase(accuracy = 2, duration = FB_trial_duration)
    this_trial += 1
    
message(message_text = 'Einde van de oefentrials, gelieve even de experimentleider te gaan halen.' + spatie)
message(message_text = 'Vanaf nu is het voor echt.' + spatie)

for increment in staircase: 
    #define opacity of the trial 
    if this_trial == n_train_trials: 
        this_opacity = start_opa
    else:
        this_opacity = increment
    #print(this_opacity)
    target_prepare(target_loc = Target_pos[this_trial], opacity = this_opacity, left_i = left_count, right_i = right_count)
    fix_type_trial = Fixation_types[int(Fixation_type_array[this_trial])]
    start_grating = Grating_start_array[this_trial]
    start_target = Target_start_array[this_trial]
    stop_target = start_target + target_frames
    max_frames = start_target + response_frames
    
    if this_trial in catch_trials: 
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
        CorResp_catch = (Fixation_type_array[this_trial] != catch_cross)*1      #if fix_type_trial == fix_type_catch, correct answer is 'f' (0)
        #print('0 / 1 for catch trial is {}'.format(CorResp_catch))
        catch_accuracy = catch_trial_feedback(correct_button = ResponseOptions[int(CorResp_catch)], 
                                          response = catch_response[0], speedy = speedy)
        print('Catch accuracy is {}'.format(catch_accuracy))
        thisExp.addData('Catch_accuracy', catch_accuracy)

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
    CorResp = ResponseOptions[int(Cor_resp[this_trial])]
    if np.all(response[0] == 'esc') or np.all(response[0] == 'escape'): 
        break
    elif np.all(CorResp == response[0]): 
        trial_accuracy, stair_accuracy = 1, 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy, stair_accuracy = 0, 0

    if Target_pos[this_trial] == 0:                        #these fucntions to adapt the position of the target inside the grating 
        left_count = left_count + 1
    else: 
        right_count = right_count + 1
    staircase.addResponse(stair_accuracy)
    #print(stair_accuracy)
    store_opa.append(this_opacity)
    store_acc.append(stair_accuracy)
    
    if speedy == 0: 
        if try_out == 0: 
            feedback_trial_staircase(accuracy = trial_accuracy, duration = FB_trial_duration)
        else: 
            feedback_trial_staircase(accuracy = 2, duration = FB_trial_duration)
    this_trial += 1
    thisExp.addData('Target_hemifield', Target_pos[this_trial])
    thisExp.addData('Opacity', this_opacity)
    thisExp.addData('Accuracy', stair_accuracy)
    thisExp.nextEntry()
    if this_trial == (n_stair_trials-1): 
        print('end reached')
        break 
    
    
message(message_text = 'Dit is het einde van het eerste deel, gelieve de experimentleider te gaan halen.')
    
    
print('test done')
win.close()

print('Opacity array: {}'.format(store_opa))
print('Accuracy array: {}'.format(store_acc))
print('Reversal array: {}'.format(staircase.reversalIntensities))
print('Mean value of all reversals is {}'.format(np.mean(staircase.reversalIntensities)))

#%% the analysis part
# set to 0.5 for Yes/No (or PSE). Set to 0.8 for a 2AFC threshold
threshVal = 0.7

# set to zero for Yes/No (or PSE). Set to 0.5 for 2AFC
expectedMin = 0.5

# get combined data
i, r, n = data.functionFromStaircase(store_opa, store_acc, bins='unique')
combinedInten, combinedResp, combinedN = i, r, n
combinedN = pylab.array(combinedN)  # convert to array so we can do maths

# fit curve
fit = data.FitWeibull(combinedInten, combinedResp, expectedMin=expectedMin,
    sems=1.0 / combinedN)
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(threshVal)
print('Treshold is: {}'.format(thresh))

stored_opa = np.array([thresh])
opacity_file = '\Stair_opacity' + str(pp_number)
np.save(my_output_directory + opacity_file + '.npy', stored_opa)

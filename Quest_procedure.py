# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:26:33 2020

@author: Maud
"""

"""
Remark on the staircase procedure
- If you answer correctly, the startVal is scaled down
  --> scaled up = more easy in  our case
  --> should work with 30-ampl: then if correct answer, will be harder; wrong answer will be more easy 
"""

import numpy as np
import math, time, os, pandas
from psychopy import visual, data, core, event

#allows to play with the staircases: only the staircases are executed, rest is skipped
speedy = 1

#%%Create the relevant stimuli & functions

#create window
win = visual.Window(size = [800, 600], units = "deg", monitor = "Laptop")

ResponseOptions = np.array(['f', 'j'])
clock = core.Clock()
clock_check = core.Clock()



#B. Create the fixation point with function                                     Fixation point
#create the fixation point              #check whether the variables are important (maybe for formula)
screen_x = 1024
screen_y = 768
screen_dis = 57 #viewing distance (cm)
screen_width = 30 #width of the screen (cm)
colorOval = "Black"
colorCross = "white"
d1 = 0.6       #diameter outer circle (degrees)
d2 = 0.2        #diameter inner circle (degrees)
r1 = d1/2
r2 = d2/2
ppd = 25 #find formula to transpose pixels to visual degrees (here pixel per degree)

point_d = math.sqrt(r1**2/2)

##problem I think: lineWidth & lineWidth are in pixels
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
def fixation_set_position(x = 0, y = 0, fix_type = 'plus'): 
    dot_b.pos = (x, y)
    dot_s.pos = (x,y)
    if fix_type == 'plus': 
        line_v.vertices = ((0+x,-r1+y),(0+x,r1+y))
        line_h.vertices = ((-r1+x,0+y),(r1+x, 0+y))
    else: 
        line_d1.vertices = ((-point_d+x, -point_d+y),(point_d+x, point_d+y))
        line_d2.vertices = ((-point_d+x, point_d+y), (point_d+x, -point_d+y))

def fixation_draw(fix = 'plus'):             #draws the fixation, does not flip it yet!
    if fix == 'plus': 
        dot_b.draw()
        line_h.draw()
        line_v.draw()
        dot_s.draw()
    else: 
        dot_b.draw()
        line_d1.draw()
        line_d2.draw()
        dot_s.draw()


#C. Create a function for the drifting gratings                                 Drifting gratings
#define some stuff
d_grating = 4
sf_grating = 1.4
pos_grating = np.array([[-5, 0], [5,0]])
GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[0])
GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])

#create a function for drifting Gratings
#define the frameTimings            (see final test 2018-2019 for more on frames)
framerate = 60

#change "Frame = 0" to the thing you iterate over in the loop!
def grating_prepare(start_oriA = 0, start_oriB = 0):
    GratingA.ori = start_oriA
    GratingB.ori = start_oriB

def grating_draw(): 
    GratingA.draw()
    GratingB.draw()

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

target_template =visual.GratingStim(win=win,tex='sin', mask='gauss',ori=0, sf=1.4, pos=(1,1), size= (1,1), interpolate=False)
left_count = 0
right_count = 0
def target_prepare(target_loc = None, amplitude = 15, left_i = left_count, right_i = right_count):         #target location: '0.0' = L, '1.0' = R
                                                                                                        #corresponds with trial['Target_hemifield']
    if target_loc == 0: 
        target_position = t_left_pos[left_i, :]
    else: 
        target_position = t_right_pos[right_i, :]
    target_template.pos = target_position
    target_template.maskParams={'sd':amplitude/2}

FB_template = visual.TextStim(win, text = '')
FB_duration = 0.5
FB_options = np.array(['Fout', 'Juist', 'Te traag'])
def feedback_trial(accuracy = 0, duration = FB_duration):        #accuracy should be matched based on acc. & block_type based on type
    FB_text = str(FB_options[accuracy])
    FB_template.text = FB_text
    FB_template.draw()
    win.flip()
    core.wait(duration)



extra_response_screen = visual.TextStim(win, text = 'Antwoord!')



#%%Staircase_instructions

spatie = '\n\n(Druk op spatie om verder te gaan)'
InstructionsP0 = str('Instructies: In deze taak zal je de locatie van een target (links of rechts) aangeven.'
                     +'De target verschijnt steeds in 1 van 2 gepresenteerde gratings (links & rechts).'
                     + 'De taak wordt in meer detail uitgelegd op volgende pagina\'s.' + spatie)
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

def instructions_stair(page = 1): 
    if page == 0: 
        instructions_text.text = InstructionsP0
        instructions_text.pos = (0, 0)
        instructions_image.image = None
    elif page == 1: 
        instructions_text.text = InstructionsP1
        instructions_text.pos = (0, 0.5)
        instructions_image.image = "Instructies_Exp1.png"
    elif page == 2: 
        instructions_text.text = InstructionsP2
        instructions_text.pos = (0, 0.5)
        instructions_image.image = "Instructies_Exp3.png"
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



#%%The timings etc.

FrameT = 1000/60

FrameT = 1000/60

#eind + 1000/60 want laatste wordt niet meegeteld & we beginnen met tellen vanaf 1 
Gr_start_limits_ms = np.array([500, 600+FrameT])         #fixation will be between 500 & 600 ms
Gr_start_limits = np.round(Gr_start_limits_ms/FrameT, 0)
Gr_start_limits.astype(int)
T_start_limits_ms = np.array([100, 2000+FrameT])
T_start_limits = np.round(T_start_limits_ms/FrameT, 0)
T_start_limits.astype(int)
T_dur_ms = 33
T_dur = int(round(T_dur_ms / FrameT, 0))

Resp_time_ms = 1000
Resp_extra_ms = 1000
Resp_time = int(round(Resp_time_ms / FrameT))
Resp_extra = int(round(Resp_extra_ms / FrameT))

#%% Create the array for staircase

#create the array for the staircase procedure
n_stair_trials = 60
Gr_start_stair = np.random.randint(Gr_start_limits[0], Gr_start_limits[1], n_stair_trials)   #the amount of frames before gratings appear 
Gr_T_interval_stair = np.random.randint(T_start_limits[0], T_start_limits[1], n_stair_trials)   #the amount of frames before gratings appear 
T_start_stair = Gr_start_stair + Gr_T_interval_stair
Gr_orientation_stair = np.random.randint(180, size = (n_stair_trials, 2))
T_hemilocaction_stair = np.repeat([0, 1], int(n_stair_trials/2))            #first 30 left, then 30 right 
Stair_target_locations = np.array([0, 1]) #0 = left, 1 = right
Stair_target_locations = np.tile(Stair_target_locations, int(n_stair_trials/2))
Stair_correct_response = np.array(Stair_target_locations == 1)*1


Stair_array = np.column_stack([Gr_start_stair, Gr_T_interval_stair, T_start_stair, Gr_orientation_stair, 
                               Stair_target_locations, Stair_correct_response])


#create experimenthandler
file_stair = "QUEST_output"
thisExp = data.ExperimentHandler(dataFileName = file_stair)

Stair_DF = pandas.DataFrame.from_records(Stair_array)     
Stair_DF.columns = ['Grating onset', 'Grating - Target interval', 'Target onset', 'Grating orientation A', 
                    'Grating orientation B', 'Target hemifield', 'Correct response']
Stair_TL = pandas.DataFrame.to_dict(Stair_DF, orient = "records")
trials = data.TrialHandler(trialList = Stair_TL, nReps = 1, method = "random")

#%%Create QuestHandler
staircase1 = data.QuestHandler(startVal = 5, startValSd = 1, nTrials = n_stair_trials/2, pTreshold = 0.70)
staircase2 = data.QuestHandler(startVal = 5, startValSd = 1, nTrials = n_stair_trials/2, pTreshold = 0.70)



#%% 

t_left_pos, t_right_pos = create_target_positions(size = n_stair_trials)
fixation_set_position(x = 0, y = 0, fix_type = 'plus')


thisExp.addLoop(trials)
fixation_set_position(x = 0, y = 0, fix_type = 'plus')

if speedy == 0: 
    for i in range(0, 6):
        instructions_stair(page = i)

for trial in trials: 
    grating_prepare(start_oriA = trial['Grating orientation A'], start_oriB = trial['Grating orientation B'])
    
    MaxFrames = trial['Target onset'] + Resp_time
    Gr_showtime = trial['Grating onset']
    T_showtime = trial['Target onset']
    T_disappeartime = T_showtime + T_dur
    
    
    #prepare for the actual staircase
    response_RT = None
    response = None
    
    if trial['Target hemifield'] == 0: 
        ampl = staircase1._nextIntensity
        trials.addData('Amplitude T Left', ampl)
    else: 
        ampl = staircase2._nextIntensity
        trials.addData('Amplitude T Right', ampl)
    
    #amplitude based on staircase
    target_prepare(target_loc = trial['Target hemifield'], amplitude = 30 - ampl, left_i = left_count, right_i = right_count)
    
    if speedy == 1: 
        response = np.array(['f'])
    else: 
        for Frame in range(MaxFrames): 
            fixation_draw()
            if Frame >= Gr_showtime: 
                grating_draw()      #function that adapts the orientation of the gratings & draws these 
            if Frame >= T_showtime and Frame < T_disappeartime: 
                target_template.draw()
            if Frame == T_showtime: 
                event.clearEvents(eventType = 'keyboard')
            win.flip()
            if Frame == T_showtime: 
                clock.reset()
            if Frame >= T_showtime: 
                response = event.getKeys(keyList = ResponseOptions, timeStamped = clock)
                response = np.array(response).squeeze()
                if len(response) != 0: 
                    break 
            
        #allow for extra response time if no response has been given yet 
        if len(response) == 0: 
            extra_response_screen.draw()
            win.flip()
            response = event.waitKeys(keyList = ResponseOptions, maxWait = Resp_extra_ms/1000, timeStamped = clock)
            response = np.array(response).squeeze()
            if np.all(response == None): 
                response = np.array([-1, -1])
                trial_accuracy, stair_accuracy = -1, 0 #for staircase make the accuracy 0 instead of -1 
                    #has to be -1 for the correct feedback
                extra_time = True
        else: 
            extra_time = False
    
    #define the accuracy 
    CorResp = trial['Correct response']
    if ResponseOptions[CorResp] == response[0]: 
        trial_accuracy, stair_accuracy = 1, 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy, stair_accuracy = 0, 0
    
    if speedy == 0: 
        feedback_trial(accuracy = trial_accuracy)
    
    #store the accuracy for the staircase
    if trial['Target hemifield'] == 0: 
        #hier de staircase aanpassen 
        left_count = left_count + 1
        staircase1.addResponse(stair_accuracy)
    else: 
        #hier de staircase aanpassen 
        right_count = right_count + 1
        staircase2.addResponse(stair_accuracy)
    
    trials.addData('Response', response[0])
    trials.addData('Accuracy', trial_accuracy)
    
    thisExp.nextEntry()

win.close()

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:26:33 2020

@author: Maud
"""

"""
QUEST opacity
* now working with adapted opacity every trial 
* amplitude is just the standard; contrast is just 1 (standard); sf = 1.4
Information
* for less trials: change n_stair_trials 
   - = total amount of trials (for staircase 1 & 2 together)
* quitting the staircase is possible: press 'escape' when allowed to respond 
* screen is at fullScreen now!
   - same problem with ppd: should be adapted to monitor values
* speedy = 1: then staircases can be tested without displaying all the visual stuff
   - just look at the output file & the adapted values for 'amplitude L & R'
   - response is automatically 'f' when speedy = 1 
"""

import numpy as np
import math, time, os, pandas
from psychopy import visual, data, core, event, gui
from Target_positions_function import create_target_positions

#allows to play with the staircases: only the staircases are executed, rest is skipped
speedy = 0

n_stair_trials = 60

#%%Create the relevant stimuli & functions
#create the gui 
# display the gui
info = { 'Naam': '','Gender': ['man', 'vrouw', 'derde gender'], 'Leeftijd': 0 , 'Participant nummer': 1}

#define directory & datafile to store information 
my_home_directory = os.getcwd()
my_directory = my_home_directory + '/' + 'data_StairCase'
if not os.path.isdir(my_directory): 
    os.mkdir(my_directory)
os.chdir(my_directory)

# make sure no repetitions of the pp_number occur
already_exists = True 
while already_exists == True: 
    info_dialogue = gui.DlgFromDict(dictionary=info, title='Information')
    pp_number = info['Participant nummer']
    datafile = 'StairCase' + str(pp_number)
    if not os.path.isfile(datafile + '.csv'): 
        already_exists = False
    else: 
        gui2 = gui.Dlg(title = 'Error')
        gui2.addText("Try another participant number")
        gui2.show()

# create the experimentHandler after storing the name for the greeting 
name = info['Naam']
# pop the name and create the experimentHandler
info.pop("Naam")

#create window
win = visual.Window(fullscr = True, units = "deg", monitor = "Laptop", mouseVisible = False)

ResponseOptions = np.array(['f', 'j', 'esc', 'escape'])
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
#ppd = 25 #find formula to transpose pixels to visual degrees (here pixel per degree)
ppd = 45 #when fullscreen on laptop use this 
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

fixation_types = np.array(['plus', 'cross'])
#create an array to shuffle each block for 50% cross and 50% plus fixation cross 
block_fixation = np.concatenate([np.zeros(int(n_stair_trials/2)), np.ones(int(n_stair_trials/2))])
#0 = plus, 1 = cross!

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

n_catchtrials = int(n_stair_trials/20) #number of catch trials for EACH block 
def catch_trials_selection(): 
    catch_trials = np.random.randint(0, n_stair_trials, n_catchtrials)
    return catch_trials

catch_question = visual.TextStim(win, text = str('Welk fixatiekruis heb je voor het laatst gezien: Het linker'
                                                 + ' of het rechter? \n Druk \'f\' als je links denkt,'
                                                 +'\'j\' als je rechts denkt'), pos = (0, 0.5), 
                                 wrapWidth = 1.9, units = 'norm')

#to display the catch trial, retutns the response that was given
#left = plus (f), right = cross (j)
catch_fix_positions = np.array([-4, 4])
def catch_trial(): 
    catch_question.draw()
    #draw the left fixation: plus
    for i, pos in enumerate(catch_fix_positions): 
        fixation_set_position(x = pos, y = 0, fix_type = fixation_types[i])
        fixation_draw(fix = fixation_types[i])
    win.flip()
    catch_response = event.waitKeys(keyList = ResponseOptions)
    for i in range(2): 
        fixation_set_position(x = 0, y = 0, fix_type = fixation_types[i])
    return catch_response


#allow to display FB on the catch trial 
FB_catch_correct = visual.TextStim(win, text = 'Juist')
FB_catch_wrong = visual.TextStim(win, text = 'Fout, probeer tijdens de trial te fixeren op het fixatiekruis')

def feedback_catch(correct_button = 0, response = None): 
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




#C. Create a function for the gratings                                 Drifting gratings
#define some stuff
d_grating = 4
sf_grating = 1.4
pos_grating = np.array([[-5, 0], [5,0]])
GratingA = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[0])
GratingB = visual.GratingStim(win, tex = 'sin', mask = 'circle', sf = sf_grating, size = d_grating, ori = 0, pos = pos_grating[1])


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

target_template =visual.GratingStim(win=win,tex='sin', mask='gauss',ori=90, sf=1.4, pos=(1,1), size= (1,1), interpolate=False)
left_count = 0
right_count = 0
def target_prepare(target_loc = None, opacity = 1, left_i = left_count, right_i = right_count, oriA = 0, oriB = 0):         #target location: '0.0' = L, '1.0' = R
                                                                                                        #corresponds with trial['Target_hemifield']
    if target_loc == 0: 
        target_position = t_left_pos[left_i, :]
        target_ori = oriA + 90
    else: 
        target_position = t_right_pos[right_i, :]
        target_ori = oriA + 90
    target_template.pos = target_position
    target_template.opacity = opacity
    target_template.ori = target_ori

FB_template = visual.TextStim(win, text = '')
FB_duration = 0.5
FB_options = np.array(['Fout', 'Juist', 'Neutral', 'Te traag'])
def feedback_trial(accuracy = 0, duration = FB_duration):        #accuracy should be matched based on acc. & block_type based on type
    FB_text = str(FB_options[accuracy])
    FB_template.text = FB_text
    FB_template.draw()
    win.flip()
    core.wait(duration)



extra_response_screen = visual.TextStim(win, text = 'Antwoord!')




#%%Staircase_instructions & greeting

#creating a template to put normal text on screen
message_template = visual.TextStim(win, text = '')
def message(message_text = '', duration = 0, response_keys = ['space'], color = 'white', height = 0.1, wrapWidth = 1.9, flip = True, position = (0,0)):
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



#%%The timings etc.

FrameT = 1000/60

FrameT = 1000/60

#eind + 1000/60 want laatste wordt niet meegeteld & we beginnen met tellen vanaf 1 
Gr_start_limits_ms = np.array([500, 600+FrameT])         #fixation will be between 500 & 600 ms
Gr_start_limits = np.round(Gr_start_limits_ms/FrameT, 0)
Gr_start_limits.astype(int)
T_start_limits_ms = np.array([500, 2000+FrameT])
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
thisExp = data.ExperimentHandler(dataFileName = datafile,  extraInfo = info)

Stair_DF = pandas.DataFrame.from_records(Stair_array)     
Stair_DF.columns = ['Grating_onset', 'Grating_Target_interval', 'Target_onset', 'Grating_orientation_A', 
                    'Grating_orientation_B', 'Target_hemifield', 'Correct_response']
Stair_TL = pandas.DataFrame.to_dict(Stair_DF, orient = "records")
trials = data.TrialHandler(trialList = Stair_TL, nReps = 1, method = "random")

#%%Create QuestHandler
staircase1 = data.QuestHandler(startVal = 0.25, startValSd = 0.10, nTrials = n_stair_trials/2, pTreshold = 0.65)
staircase2 = data.QuestHandler(startVal = 0.25, startValSd = 0.10, nTrials = n_stair_trials/2, pTreshold = 0.65)



#%% 

t_left_pos, t_right_pos = create_target_positions(size = n_stair_trials)
fixation_set_position(x = 0, y = 0, fix_type = 'plus')


thisExp.addLoop(trials)

message(message_text = greeting, duration = 1)
if speedy == 0: 
    for i in range(0, 6):
        instructions_stair(page = i)

grating_prepare(start_oriA = 0, start_oriB = 0)
n_train_trials = 10
train_appear = np.random.randint(30, 121, n_train_trials)
train_target = np.random.randint(0, 2, n_train_trials)
train_fix = np.random.randint(0, 2, n_train_trials)
train_gratingT = 2
left_count = 7
right_count = 10
message(message_text = 'Dit is een oefen-deel' + spatie)
for i in range(n_train_trials): 
    fix_type = fixation_types[train_fix[i]]
    train_targetT = train_appear[i]
    target_prepare(target_loc = train_target[i], opacity = 0.3, left_i = left_count, right_i = right_count, 
            oriA = 0, oriB = 0)
    for frame in range(train_appear[i] + Resp_time): 
        fixation_draw(fix = fix_type)
        if frame >= train_gratingT: 
            grating_draw()
        if frame >= train_targetT and frame < (train_targetT+2): 
            target_template.draw()
        win.flip()
        if frame == train_targetT: 
            event.clearEvents(eventType = 'keyboard')
            clock.reset()
        if frame >= train_targetT: 
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
            response = np.array([-1])
            trial_accuracy = -1 #for staircase make the accuracy 0 instead of -1 
                #has to be -1 for the correct feedback
        extra_time = True
    else: 
        extra_time = False
    
    #define the accuracy 
    CorResp = train_target[i]
    if ResponseOptions[CorResp] == response[0]: 
        trial_accuracy = 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy = 0
    feedback_trial(accuracy = trial_accuracy)
    left_count += 1
    right_count += 1
        
    
message(message_text = 'Vanaf nu is het voor echt.' + spatie)
np.random.shuffle(block_fixation)
catch_trials = catch_trials_selection()
#catch_trials = np.array([1, 2, 3, 4, 5])   # is enkel om te testen 
this_stair_trial = 0
left_count = 0
right_count = 0
for trial in trials: 
    #grating_prepare(start_oriA = trial['Grating_orientation_A'], start_oriB = trial['Grating_orientation_B'])
    MaxFrames = trial['Target_onset'] + Resp_time
    Gr_showtime = trial['Grating_onset']
    T_showtime = trial['Target_onset']
    T_disappeartime = T_showtime + T_dur
    
    
    #prepare for the actual staircase
    response_RT = None
    response = None
    
    fix_type_bin = int(block_fixation[this_stair_trial])
    fix_type = fixation_types[fix_type_bin]
    fixation_set_position(x = 0, y = 0, fix_type = fix_type)
    
    if trial['Target_hemifield'] == 0: 
        opa = staircase1._nextIntensity
        trials.addData('Opacity_T_Left', opa)
    else: 
        opa = staircase2._nextIntensity
        trials.addData('Opacity_T_Right', opa)
    
    #opacity based on staircase
#    target_prepare(target_loc = trial['Target_hemifield'], opacity = opa, left_i = left_count, right_i = right_count,
#        oriA = trial['Grating_orientation_A'], oriB = trial['Grating_orientation_B'])
    target_prepare(target_loc = trial['Target_hemifield'], opacity = opa, left_i = left_count, right_i = right_count, 
        oriA = 0, oriB = 0)
    #add the catch-trials
    if this_stair_trial in catch_trials: 
        if speedy == 0: 
            for Frame in range(1, 60): 
                fixation_draw(fix = fix_type)
                if Frame > 33: 
                    grating_draw()
                win.flip()
            catch_response = catch_trial()
        else: 
            catch_response = np.array(['f'])
        catch_accuracy = feedback_catch(correct_button = ResponseOptions[int(fix_type_bin)], 
                                      response = catch_response[0])
        trials.addData('catch_accuracy', catch_accuracy)
        
    
    
    if speedy == 1: 
        response = np.array(['f'])
    else: 
        for Frame in range(MaxFrames): 
            fixation_draw(fix = fix_type)
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
    CorResp = trial['Correct_response']
    if response[0] == 'esc' or response[0] == 'escape': 
        break
    elif ResponseOptions[CorResp] == response[0]: 
        trial_accuracy, stair_accuracy = 1, 1
    elif response[0] == -1: 
        pass
    else: 
        trial_accuracy, stair_accuracy = 0, 0
    
    if speedy == 0: 
        feedback_trial(accuracy = trial_accuracy)
        #feedback_trial(accuracy = 2)
    #store the accuracy for the staircase
    if trial['Target_hemifield'] == 0: 
        #hier de staircase aanpassen 
        left_count = left_count + 1
        staircase1.addResponse(stair_accuracy)
    else: 
        #hier de staircase aanpassen 
        right_count = right_count + 1
        staircase2.addResponse(stair_accuracy)
    
    trials.addData('Response', response[0])
    trials.addData('Accuracy', trial_accuracy)
    
    if this_stair_trial == n_stair_trials - 1: 
        trials.addData('QuantileL', np.round(staircase1.quantile(), 2))
        trials.addData('QuantileR', np.round(staircase2.quantile(), 2))
        trials.addData('MeanL', np.round(staircase1.mean(), 2))
        trials.addData('MeanR', np.round(staircase2.mean(), 2))
    
    thisExp.nextEntry()
    this_stair_trial += 1

win.close()

stored_opa = np.array([np.round(staircase1.quantile(), 2), np.round(staircase2.quantile(), 2)])
opacity_file = 'Stair_opacity' + str(pp_number)
np.save(opacity_file + '.npy', stored_opa)

print(staircase1.mean(), staircase2.mean())
print(staircase1.quantile(), staircase2.quantile())
print(staircase1.median(), staircase2.median())

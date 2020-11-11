# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 12:23:20 2020

@author: Maud
"""

#import the relevant modules
from psychopy import visual, data, event, core, gui
import os, pandas, math
import numpy as np

#Info: verander n_blocktrials om het aantal trials per block te wijzigen (lijn 28)
#Info: speedy = 1, door het experiment rushen, de frame-timings worden wel volledig afgespeeld, 
    #dit om makkelijker te kijken of de timings correct zijn (lijn 11)
#Info: de monitor bij het definieren van de window moet wss ook nog aangepast worden (lijn 49)

#allow to speed through the experiment
speedy = 0

#Create the general block array that will be used each block                    #Part 1
#Create an array with all possible combinations 
Target_Relative_Options = np.array(["S", "O"])               #This is the congruency in fact 
Flash_Options = np.array(["L", "R"])
FTI = np.arange(-15, 48, 3)

AllOptions = np.array(np.meshgrid(FTI, Flash_Options, Target_Relative_Options)).T.reshape(-1,3)
##This contains all possible combinations of FTI, Flash_pos & Flash-Target pos
##Idea: per block all these combinations occur
    ## So amount of blocks: 1 * 2 * 3 (--> 2 for R / NR; 3 for 3 times each possible combination)


#Add the CorResp to the array 
n_blocktrials = AllOptions.shape[0]
n_blocktrials = 4                      #this is added to run the experiment with only 2 trials, this for programming 
CorResp = np.zeros(shape = AllOptions.shape[0])
for i in range(AllOptions.shape[0]):          #0 = "f" / L; 1 = "j" / R
    if (AllOptions[i, 1] == "L" and AllOptions[i,2] == "S") or (AllOptions[i, 1] == "R" and AllOptions[i,2] == "O"): 
        CorResp[i] = 0
    else: 
        CorResp[i] = 1
AllOptions = np.column_stack([AllOptions, CorResp])          #Add the CorResp as 4th column in the array 
Target_location = np.copy(CorResp)          #both are the same since response - position mapping is always congruent in this experiment
AllOptions = np.column_stack([AllOptions, Target_location])


#define the amount of trials & blocks
n_blocks = 2
n_trials = n_blocks*n_blocktrials



#Part 2: define all the relevant stimuli                                                            #Part 2: relevant stimuli over all blocks

#A. Some general stuff                                                          General stuff 
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

fixation_types = np.array(['plus', 'cross'])

#fix = '' should be filled in with the type for that trial
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

#create an array to shuffle each block for 50% cross and 50% plus fixation cross 
block_fixation = np.concatenate([np.zeros(int(n_blocktrials/2)), np.ones(int(n_blocktrials/2))])
#0 = plus, 1 = cross!




n_catchtrials = 5 #number of catch trials for EACH block 
def catch_trials_selection(): 
    catch_trials = np.random.randint(0, n_blocktrials, n_catchtrials)
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
def grating_prepare(start_oriA = 0, start_oriB = 0, driftRate = 0.7, direction = 0):
        #standard for start_oriA & B = random location (this can be used to define where to start) (= the first appearance in each trial should be standard)
        #change "Frame = 0" to the thing you iterate over in the loop!
    drift_per_frame = 180*driftRate / framerate   #1 cycle = 180; 0.7 = the wanted drift amount per second; framerate = we flip every frame
    if direction == 0: 
        drift_per_frame = -drift_per_frame
    else: 
        drift_per_frame = drift_per_frame
    GratingA.ori = start_oriA 
    GratingB.ori = start_oriB 
    return start_oriA, start_oriB, drift_per_frame

def grating_draw(): 
    GratingA.ori+= drift_per_frame
    GratingB.ori+= drift_per_frame
    GratingA.draw()
    GratingB.draw()



#D. Creating the flash                                                          Flash 

#create a function to create arrays that contain the positions of the dots for both left & right flash 
def create_flashpos_arrays():                           #function that returns 2 arrays with the pos_values for 4 dots for both left & right flash 
    flash_positions = np.array(['L', 'R'])
    for i in range(flash_positions.shape[0]): 
        if flash_positions[i] == 'L': 
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
            dot_flashP_L = np.array([dot_left, dot_right, dot_up, dot_down])
        else: 
            dot_flashP_R = np.array([dot_left, dot_right, dot_up, dot_down])
    return dot_flashP_L, dot_flashP_R
    
flash_left, flash_right = create_flashpos_arrays()         #This is how to use the function "create_flashpos_arrays()"
                                                            #(not !! to use this function anymore after this line)
dot_template1 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
dot_template2 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
dot_template3 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
dot_template4 = visual.Circle(win, color = 'white', radius = 0.5, fillColor = 'white')
#create a function to display the flash 
def flash_prepare(position = 'L', n_dots = 4):                  # in trialloop: "position = 'L'" should be replaced by "position = trial[flash_position]"
    if position == 'L': 
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
    dot_template1.draw()
    dot_template2.draw()
    dot_template3.draw()
    dot_template4.draw()
    
# E. Create the Target                                                          Target
def create_target_positions(size = n_blocktrials): 
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
def target_prepare(target_loc = '0.0', amplitude = 15, left_i = left_count, right_i = right_count):         #target location: '0.0' = L, '1.0' = R
                                                                                                        #corresponds with trial['Target_hemifield']
    if target_loc == '0.0': 
        target_position = t_left_pos[left_i, :]
    else: 
        target_position = t_right_pos[right_i, :]
    target_template.pos = target_position
    target_template.maskParams={'sd':amplitude/2}


extra_response_screen = visual.TextStim(win, text = 'Antwoord!')
    
    
#picture that clarifies the experiment to the participant
#design_pic = visual.ImageStim(win, image = "Design_staircase.jpg", pos = (0, -0.5), units = 'norm')


#Part 4: Define timings that can be defined before hand                                                                                 Part 4: Fixed Timings

#The timings that can be defined beforehand
#Define the timings that are constant over the whole experiment
FrameT = 1000/60
Gr_start_limits_ms = np.array([500, 600])         #fixation will be between 500 & 600 ms
Gr_Fl_limits_ms = np.array([750, 1250])    #Gratings will appear for 750 - 1250 ms before flash occurs
Fl_dur_ms = 33
T_dur_ms = 33
Resp_time_ms = 1000
Resp_extra_ms = 1000

#Define the timings in Frames
Gr_start_limits = np.round(Gr_start_limits_ms/FrameT, 0)
Gr_start_limits.astype(int)
Gr_Fl_limits = Gr_Fl_limits_ms/FrameT
Gr_Fl_limits.astype(int)
Fl_dur = int(round(Fl_dur_ms / FrameT, 0))
T_dur = int(round(T_dur_ms / FrameT, 0))
Resp_time = int(round(Resp_time_ms / FrameT))
Resp_extra = int(round(Resp_extra_ms / FrameT))



#Part 5: define functions for interaction with pp                                                               Part 5: functions for interaction with pp. 

#create the gui 
# display the gui
info = { 'Naam': '','Gender': ['man', 'vrouw', 'derde gender'], 'Leeftijd': 0 , 'Participant nummer': 1}

#define directory & datafile to store information 
my_home_directory = os.getcwd()
my_directory = my_home_directory + '/' + 'data_Experiment'
if not os.path.isdir(my_directory): 
    os.mkdir(my_directory)
os.chdir(my_directory)

# make sure no repetitions of the pp_number occur
already_exists = True 
while already_exists == True: 
    info_dialogue = gui.DlgFromDict(dictionary=info, title='Information')
    pp_number = info['Participant nummer']
    datafile = 'data_allBlocks' + str(pp_number)
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

#Create the experiment Handler
# Start the ExperimentHandler, add the output file name and store the dialog box info (without the participant name!)
file_name = datafile
thisExp = data.ExperimentHandler(dataFileName = file_name, extraInfo = info)


#define the feedback & the instructions
points_per_euro = 1000
points_per_trial = 10


#The instructions (in Dutch)
spatie = '\n\n(Druk op spatie om verder te gaan)'
greeting = "Hallo " + name + spatie
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
                     + '\nDoe dit zo snel, maar vooral ook zo ACCURAAT mogelijk.' + spatie)
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
def instructions(page = 1): 
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
        instructions_image.image = "Instructies_Exp2.png"
    elif page == 3: 
        instructions_text.text = InstructionsP3
        instructions_text.pos = (0, 0.5)
        instructions_image.image = "Instructies_Exp3.png"
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


#Create the sequence of the blocks (counterbalanced over pp.)
block_sequence = np.array([['REWARD', 'NON REWARD'], ['NON REWARD', 'REWARD']])
block_type_array = np.tile(block_sequence[pp_number%2], int(n_blocks/2))


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

FB_template = visual.TextStim(win, text = '')
FB_duration = 0.5
FB_options = np.array(['Fout', 'Juist', 'Te traag'])
points = np.array(['+0', str('+' + str(points_per_trial)), '+0'])          #wrong, correct, no answer given 
def feedback_trial(block_type = 'REWARD', accuracy = 0, duration = FB_duration):        #accuracy should be matched based on acc. & block_type based on type
    if block_type == 'REWARD': 
        FB_text = str(FB_options[accuracy] + " " + points[accuracy])
    else: 
        FB_text = str(FB_options[accuracy] + " " + points[0])
    FB_template.text = FB_text
    FB_template.draw()
    win.flip()
    if speedy == 1: 
        core.wait(0.1)
    else: 
        core.wait(duration)

FB_block_duration = 2
total_points = 0
def feedback_block(durationR = FB_block_duration, block_type = 'REWARD', blockP = 0, totalP = 0):
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



message(message_text = greeting)
for i in range(0, 8): 
    instructions(page = i)

points_total = 0
trial_count = 0


for block in range(n_blocks): 
    #random shuffle the block, so we can obtain the FTI values beforehand to define block_timings beforehand as well 
    np.random.shuffle(AllOptions)
    Block_array = AllOptions
    #creation of the trialloop + validation of the dataframe
    Block_DF = pandas.DataFrame.from_records(Block_array)     #this is only used to check the randomization, for the validation see above
    Block_DF.columns = ['FTI', 'Flash_position', 'CongruencyFl_T', 'CorResp', 'Target_position']
    validation = pandas.crosstab([Block_DF.Flash_position, Block_DF.Target_position], Block_DF.FTI)
    validation_file = 'Validation' + str(block) + '.csv'
    validation.to_csv(validation_file, index = True)
    DF_file = 'Block_design_shuffled' + str(block) + '.csv'
    Block_DF.to_csv(DF_file, index = True)
    
    
    #Define the timings that variate per block 
    Gr_start_array = np.random.randint(Gr_start_limits[0], Gr_start_limits[1], AllOptions.shape[0])   #the amount of frames before gratings appear 
    #print(Gr_start_array)
        #problem: returns values of 29 as well, how is this possible???                                     !!!!!!!!!!!
        #think it is okay cause python starts counting from 0 onwards
        ##To get Random integers array of type NumPy int between low and high, inclusive.
    Gr_Fl_array = np.random.randint(Gr_Fl_limits[0], Gr_Fl_limits[1], AllOptions.shape[0]) #amount of frames between Grating & Flash 
    #print(Gr_Fl_array)
    FTI_array = Block_array[:, 0] #amount of frames between flash & target appearance 
    FTI_array = FTI_array.astype(int)         #make sure the values stored are floats, to be able to add with another array later on 
    #Define all the total Frames for each trial for this block 
    #all the below mentioned variables are arrays of shape [, 84], these can be used for each trial 
    Gr_start = Gr_start_array    #how long after fixation gratings should appear (in Frames)
    Fl_start = np.add(Gr_start, Gr_Fl_array)    #when the flash should appear  (in Frames)
    T_start = np.add(Fl_start, FTI_array)   #when the target should appear (in Frames)
    Max_Frames = T_start + Resp_time   #the maximum amount of Frames when no reponse is given earlier, if no response, still extra time given
            #is an array with 84 values (shape = [, 84]), 1 value  for each trial
    
    #define an array with directions of the gratings turn-patter for each trial          (Could be done beforehand as well)
    Gr_directions = np.random.randint(2, size = n_blocktrials)
    
    #define an array with the starting values for each grating for each trial
    gr_orientation_start_array = np.random.randint(180, size = (AllOptions.shape[0], 2))
    
    #define the the positions of the target inside the gratings for either L or R targets 
    t_left_pos, t_right_pos = create_target_positions(size = n_blocktrials*2) #voor testversie even *2, want mogelijk dat meer dan de helft van de trials target
                #links of rechts hebben; voor echte versie is het gwn 'n_blocktrials'
    #this is !! to later use the function 'target_draw()'
    left_count = 0
    right_count = 0
    
    #shuffle what fixation cross will be displayed each trial
    np.random.shuffle(block_fixation)
    
    
    #define an array with when the catch trials will appear this block: 
    catch_trials = catch_trials_selection()
    catch_trials = np.array([2, 4]) #is even om te testen 
    
    
    #Create the trialloop
    DesignTL = pandas.DataFrame.to_dict(Block_DF, orient = "records")
    trials = data.TrialHandler(trialList = DesignTL, nReps = 1, method = "sequential")
    thisExp.addLoop(trials)
    
    #allow to count the trials for each block 
    this_blocktrial = 0
    #allow to count the points earned in each block 
    points_this_block = 0
    #the type of the current block 
    this_block_type = block_type_array[block]
    #announce the start of the block 
    message(message_text = str("Dit is blok {0}. Dit is een {1} blok.".format(block + 1, this_block_type) 
                               + "\n Druk \'spatie\' om te starten."))
    
    
    #start the loop
    for trial in trials: 
        response_RT = None
        response = None
        win.recordFrameIntervals = True
        win.refreshThreshold = 1/framerate + 0.004
        
        #prepare the values of the stimuli for this trial
        flash_prepare(position = trial["Flash_position"])
        target_prepare(target_loc = trial['Target_position'], left_i = left_count, right_i = right_count)
        start_oriL, start_oriR, drift_per_frame = grating_prepare(direction = Gr_directions[this_blocktrial], 
                            start_oriA = gr_orientation_start_array[this_blocktrial, 0], start_oriB = gr_orientation_start_array[this_blocktrial, 1])
        
        #prepare the start- and end-points for this trial
        start_grating = Gr_start[this_blocktrial]
        start_flash = Fl_start[this_blocktrial]
        stop_flash = Fl_start[this_blocktrial] + Fl_dur
        start_target = T_start[this_blocktrial] 
        stop_target = T_start[this_blocktrial] + T_dur
        
        fix_type_bin = int(block_fixation[this_blocktrial])
        fix_type = fixation_types[fix_type_bin]
        
        clock_check.reset()

        for Frame in range(1, Max_Frames[this_blocktrial]):
            fixation_draw(fix = fix_type)
            if Frame >= start_grating: 
                grating_draw()
                
            if Frame >= start_flash and Frame < stop_flash: 
                flash_draw()
            if Frame >= start_target and Frame < stop_target:
                target_template.draw()
            win.flip()
            #reset the clock once the target is displayed
            if Frame == start_target: 
                clock.reset()
                event.clearEvents(eventType = 'keyboard')
            #check whether the timings are correct 
            if Frame == start_grating: 
                Gr_appearT = clock_check.getTime()
            elif Frame == start_flash:
                Fl_appearT = clock_check.getTime()
            elif Frame == stop_flash: 
                Fl_stopT = clock_check.getTime()
            if Frame == start_target: 
                T_appearT = clock_check.getTime()
            elif Frame == stop_target: 
                T_stopT = clock_check.getTime()
            
            if Frame >= start_target: 
                response = event.getKeys(keyList = ResponseOptions, timeStamped = clock)
                response = np.array(response).squeeze()
                if speedy == 1 and Frame >= stop_flash and Frame >= stop_target: 
                    response = np.array(['f', 0])
                if len(response) != 0:
                    break 
        print('Overall, %i frames were dropped.' % win.nDroppedFrames)
        total_frames_dropped = win.nDroppedFrames
        win.recordFrameIntervals = False
        #allow for extra response time if no response is given yet
        if len(response) == 0:
            extra_response_screen.draw()
            win.flip()
            response = event.waitKeys(keyList = ResponseOptions, maxWait = Resp_extra_ms/1000, timeStamped = clock)
            response = np.array(response).squeeze()
            if np.all(response == None): 
                response = np.array([-1, -1])
                trial_accuracy = -1
            extra_time = True
        else: 
            extra_time = False
        
        if (response[0] == 'f' and trial['CorResp'] == '0.0') or (response[0] == 'j' and trial['CorResp'] == '1.0'):
            trial_accuracy = 1
        elif (response[0] == 'f' and trial['CorResp'] != '0.0') or (response[0] == 'j' and trial['CorResp'] != '1.0'): 
            trial_accuracy = 0
            
        
        feedback_trial(accuracy = trial_accuracy, block_type = this_block_type)
        if this_block_type == 'REWARD' and trial_accuracy == 1: 
            points_this_block = points_this_block + points_per_trial
            points_total = points_total + points_per_trial
        
        if this_blocktrial in catch_trials: 
            catch_response = catch_trial()
            catch_accuracy = feedback_catch(correct_button = ResponseOptions[int(fix_type_bin)], 
                                      response = catch_response[0])
            trials.addData('catch accuracy', catch_accuracy)
        
        
        #Add relevant data to the stored output_file
        
        trials.addData('Block type', this_block_type)
        trials.addData('Block_n', block)
        trials.addData('Blocktrial number', this_blocktrial)
        trials.addData('Trial number', trial_count)
        trials.addData('Response', response[0])
        trials.addData('Accuracy', trial_accuracy)
        trials.addData('RT', response[1])
        trials.addData('Extra time needed', extra_time)
        trials.addData('Total points', points_total)
        trials.addData('Block points', points_this_block)
        trials.addData('Grating direction', Gr_directions[this_blocktrial])
        trials.addData('Start ori grating L', start_oriL)
        trials.addData('Start ori grating R', start_oriR)
        trials.addData('Grating start F', Gr_start[this_blocktrial])
        trials.addData('Flash start F', Fl_start[this_blocktrial])
        trials.addData('Target start F', T_start[this_blocktrial])
        trials.addData('FTI check', T_start[this_blocktrial] - Fl_start[this_blocktrial])
        #below: to be able to validate the timings of the different stimuli events in ms 
        trials.addData('Gr appear T', Gr_appearT)
        trials.addData('Fl appear T', Fl_appearT)
        trials.addData('Fl stop T', Fl_stopT)
        trials.addData('T appear T', T_appearT)
        trials.addData('T stop T', T_stopT)
        trials.addData('Total Dropped Frames', total_frames_dropped)
        
        
        #allow to store the next entry 
        thisExp.nextEntry()
        #this is !! for the function target_draw() to select the right value from the target_position_arrays 
                #L or R 
        if trial['CorResp'] == '0.0': 
            left_count = left_count + 1
        else: 
            right_count = right_count + 1
        this_blocktrial = this_blocktrial + 1
        trial_count = trial_count + 1
        if this_blocktrial == n_blocktrials:    #allow to run the experiment with less trials than 84 per block 
            break
    feedback_block(durationR = FB_block_duration, block_type = this_block_type, blockP = points_this_block, 
                   totalP = points_total)
    
win.close()

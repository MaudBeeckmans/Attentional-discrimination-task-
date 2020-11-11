# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 12:39:55 2020

@author: Maud
"""


from psychopy import visual, core, data, event
import os 

win=visual.Window([700,500], units='deg', monitor='Laptop')

grating1=visual.GratingStim(win,tex='sin',mask="circle", ori=120, sf=1.4, pos=(0,0), size= (4,4), interpolate=False)
grating2=visual.GratingStim(win,tex='sin', mask='gauss',ori=0, sf=1.4, pos=(1,1), size= (1,1), interpolate=False)


#staircase1 = data.QuestHandler(startVal = 15, startValSd = 10, nTrials =30, pTreshold = 0.70)
staircase1 = data.QuestHandler(startVal = 7, startValSd = 7, nTrials =30, pTreshold = 0.70)

trial = staircase1.thisTrialN
while trial < staircase1.nTrials: 
    ampl = staircase1._nextIntensity
    #grating2.maskParams={'sd':ampl/2}
    grating2.maskParams={'sd':ampl}
    grating1.draw()
    grating2.draw()
    win.flip()
    response = event.waitKeys(keyList = ['f', 'j'])
    if response[0] == 'f': 
        accuracy = 1
    else: 
        accuracy = 0
    staircase1.addResponse(accuracy)
    ampl = staircase1._nextIntensity
    print(ampl)
    trial = trial+1
    print(accuracy)

directory = os.getcwd()
staircase1.saveAsExcel(directory + '\Test')

win.close()
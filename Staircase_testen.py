from psychopy import visual, data, event, core, gui
import numpy as np


n_trials = 84
n_blocks = 2
Opa_array = np.empty([n_blocks, int(n_trials/2)])

responses = np.concatenate([np.ones(35), np.zeros(42-35)])
responses = responses.astype(int)
np.random.shuffle(responses)

#%%Test differences in Tresholds
Tresholds = np.array([0.60, 0.70])
for block in range(n_blocks): 
    Tres = Tresholds[block]
    staircase1 = data.QuestHandler(startVal = 0.25, startValSd = 0.15, nTrials = n_trials/2, 
                                   pTreshold = Tres)
    for i in range(int(n_trials/2)): 
        Opa_array[block, i] = staircase1._nextIntensity
        resp = responses[i]
        staircase1.addResponse(resp)
    print('The staircase output with pTreshold = {}'.format(Tres))
    print(staircase1.mode(), staircase1.quantile())

print('StartValSd = {0}; pTreshold = {1}'.format(staircase1.startValSd, Tresholds))
print('Difference between the 2 created intensity_arrays')
print(Opa_array[0] - Opa_array[1])

#%% Test differences in StartValSd
StartVals = np.array([0.15, 0.25])
for block in range(n_blocks): 
    Tres = 0.7
    StartVal = StartVals[block]
    staircase1 = data.QuestHandler(startVal = 0.25, startValSd = StartVal, nTrials = n_trials/2, 
                                   pTreshold = Tres)
    for i in range(int(n_trials/2)): 
        Opa_array[block, i] = staircase1._nextIntensity
        resp = responses[i]
        staircase1.addResponse(resp)
    print('The staircase output with StartValSD = {}'.format(StartVal))
    print(staircase1.mode(), staircase1.quantile())

print('StartValSd = {0}; pTreshold = {1}'.format(StartVals, Tres))
print('Difference between the 2 created intensity_arrays')
print(Opa_array[1] - Opa_array[0])

# The staircase output with pTreshold = 0.6
# 0.15 0.15895415416901465
# The staircase output with pTreshold = 0.7
# 0.15 0.15895415416901465
# StartValSd = 0.15; pTreshold = [0.6 0.7]
# Difference between the 2 created intensity_arrays
# [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
#  0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
# The staircase output with StartValSD = 0.15
# 0.15 0.15895415416901465
# The staircase output with StartValSD = 0.25
# 0.07 0.08103633482781789
# StartValSd = [0.15 0.25]; pTreshold = 0.7
# Difference between the 2 created intensity_arrays
# [ 0.         -0.01161444 -0.03697924 -0.05643591 -0.07301029 -0.08757491
#  -0.04311157 -0.05301943 -0.05970501 -0.06471628 -0.06833997 -0.0714618
#  -0.07398071 -0.07608256 -0.07790599 -0.07951899 -0.08114998 -0.0827677
#  -0.08429862 -0.08590888 -0.08019929 -0.08112822 -0.08192523 -0.0827822
#  -0.07902572 -0.07970497 -0.08030679 -0.07782528 -0.07827764 -0.07880101
#  -0.07913167 -0.07742954 -0.07589964 -0.07643212 -0.07668864 -0.07718949
#  -0.07744773 -0.07785238 -0.07811267 -0.07825499 -0.07858643 -0.07766049]




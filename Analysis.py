# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:52:19 2021

@author: Maud
"""

import numpy as np 
import os
import pandas as pd 
import matplotlib.pyplot as plt
file = os.path.join(os.getcwd(), "output", "Outputfile_pp7300.csv")

#create Block_type column for this data set (wasn't included here) 
REW_BlockT = np.repeat('REWARD', 84)
NONREW_BlockT = np.repeat('NON REWARD', 84)
Block_t = np.concatenate([REW_BlockT, NONREW_BlockT])
Block_t = np.tile(Block_t, 3)


#%% Create the useful_data
df = pd.read_csv(file)
df.insert(7, 'Block_type', Block_t)
useful_data = df[['BlockN', 'FTI', 'Flash_position', 'Target_relative_position', 'Accuracy', 'RT', 'Block_type']]

np_data = useful_data.to_numpy()

pos_values = np.arange(0, 46, 3)
neg_values = np.arange(-15, 0, 3)
pos_FTI = useful_data.loc[useful_data['FTI'].isin(pos_values)]
neg_FTI = useful_data.loc[useful_data['FTI'].isin(neg_values)]

#%% Create the different data per condition (R / nonR; T same / opp; flash L /R)
#split into Reward & non-Reward
def split_Reward(data = None, column_name = 'Block_type'): 
    Rew = data.loc[data[column_name] =='REWARD']
    Non_Rew = data.loc[data[column_name] =='NON REWARD']
    return Rew, Non_Rew
pos_rew, pos_nonrew = split_Reward(data = pos_FTI)

def split_Target_rel(data = None, column_name = 'Target_relative_position'): 
    Same = data.loc[data[column_name] ==0]
    Opp = data.loc[data[column_name] ==1]
    return Same, Opp
pos_rew_same, pos_rew_opp = split_Target_rel(data = pos_rew)
pos_nonrew_same, pos_nonrew_opp = split_Target_rel(data = pos_nonrew)

def split_Flash(data = None, column_name = 'Flash_position'): 
    Flash_L = data.loc[data[column_name] ==0]
    Flash_R = data.loc[data[column_name] ==1]
    return Flash_L, Flash_R
pos_rew_same_flL, pos_rew_same_flR = split_Flash(data = pos_rew_same)
pos_nonrew_same_flL, pos_nonrew_same_flR = split_Flash(data = pos_nonrew_same)
pos_rew_opp_flL, pos_rew_opp_flR = split_Flash(data = pos_rew_opp)
pos_nonrew_opp_flL, pos_nonrew_opp_flR = split_Flash(data = pos_nonrew_opp)

#%% compute the mean for each FTI & plot the results
def mean_per_FTI(data = None, column_name = 'FTI'):
    n_FTI = len(np.unique(data[column_name]))
    mean_array = np.empty([n_FTI, 3])
    for count, i in enumerate(np.unique(data[column_name])): 
        test = data.loc[data[column_name] ==i]
        mean_array[count, :] = np.array([i, np.mean(test['Accuracy']), np.mean(test['RT'])])
    return mean_array
# all 8 conditions
mean_pos_rew_same_flL = mean_per_FTI(data = pos_rew_same_flL)
mean_pos_rew_same_flR = mean_per_FTI(data = pos_rew_same_flR)
mean_pos_rew_opp_flL = mean_per_FTI(data = pos_rew_opp_flL)
mean_pos_rew_opp_flR = mean_per_FTI(data = pos_rew_opp_flR)
mean_pos_nonrew_same_flL = mean_per_FTI(data = pos_nonrew_same_flL)
mean_pos_nonrew_same_flR = mean_per_FTI(data = pos_nonrew_same_flR)
mean_pos_nonrew_opp_flL = mean_per_FTI(data = pos_nonrew_opp_flL)
mean_pos_nonrew_opp_flR = mean_per_FTI(data = pos_nonrew_opp_flR)

#%% plot the mean accuracy data
def plot_mean_accuracy(data = None): 
    fig, axes = plt.subplots(nrows = 1, ncols = 1)
    axes.set_title('Plot of mean accuracy')
    axes.plot(data[:, 0].astype(int), data[:, 1])

plot_mean_accuracy(data = mean_pos_rew_same_flL)
plot_mean_accuracy(data = mean_pos_rew_same_flR)
plot_mean_accuracy(mean_pos_rew_opp_flL)
plot_mean_accuracy(mean_pos_rew_opp_flR)
plot_mean_accuracy(mean_pos_nonrew_same_flL)
plot_mean_accuracy(mean_pos_nonrew_same_flR)
plot_mean_accuracy(mean_pos_nonrew_opp_flL)
plot_mean_accuracy(mean_pos_nonrew_opp_flR)

#%%create fourier transform of the data
def fourier_transform(data = None): 
    time_points = data[:, 0]*1/60
    ft = np.fft.fft(data[:, 1])
    return time_points, ft
time_points, ft = fourier_transform(data = mean_pos_rew_same_flL)
average_data = mean_pos_rew_same_flL[:, 1]
plt.psd(average_data, Fs = 20)




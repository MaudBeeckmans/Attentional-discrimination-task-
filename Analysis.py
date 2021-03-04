# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 08:52:19 2021

@author: Maud
"""

import numpy as np 
import os
import pandas as pd 
import matplotlib.pyplot as plt
from scipy import stats
number_pp = 35
pplist = np.arange(1,36)
for number in pplist: 
    file = os.path.join(os.getcwd(), "Output_files", "Outputfile_pp" + str(number) + ".csv")
    df = pd.read_csv(file, sep = ',')
    update_data = df[['BlockN', 'FTI', 'Flash_position', 'Target_relative_position', 'Accuracy', 'Catch_accuracy', 'RT', 'Block_type', 'Participant nummer']]
    if number == 1: 
        useful_data = update_data
    else: 
        useful_data = useful_data.append(update_data)
        

#%%

print('\nColumn names of datafile')
print(useful_data.columns)
# Index(['BlockN', 'FTI', 'Flash_position', 'Target_relative_position',
#        'Accuracy', 'Catch_accuracy', 'RT', 'Block_type', 'Participant nummer'],
#       dtype='object')
np_data = useful_data.to_numpy()

"""Add a column with FTI > 0 vs. FTI < 0 for the Anova"""
When_flash = (np_data[:,1].astype(float)>=0)*1  #0 = before, 1 = after

np_data = np.column_stack([np_data, When_flash])

#%%preprocess the raw data columns
"""replace response strings with response time""" 
count = 0
for i in np_data[:, 6]: 
    if type(i) != float: 
        if ('f' in i or 'j' in i): 
            np_data[count, 6] = float(i[6:-2])
        else: 
            np_data[count, 6] = float(i)
    count +=1

#replace pp_number by correct number
np_data[:, 8] = np.where(np_data[:, 8] > 100, np_data[:, 8] - 100, np_data[:, 8])
        
        
#%%
"""create the correct classes (float / integer / string)"""

print('\nFirst row of Data')
print(np_data[0,:])
np_data[:, :5] = np_data[:, :5].astype(int)
np_data[:, 6] = np_data[:, 6].astype(float)
print(type(np_data[0, 4]))

#%% delete participants based on different items 

"""delete pp with catch accuracy < 70%"""

Catch_trials = np_data[~np.isnan(np_data[:,5].astype(float)),:]
Catch_trials = Catch_trials[:,np.array([5,8])].astype(float)
Catch_accuracy = [np.mean(Catch_trials[Catch_trials[:,1]==i,0])*100 for i in pplist]

remove_participants = pplist[np.array(Catch_accuracy)<70]
pplist2 = np.delete(np.array(pplist),remove_participants-1)

print("\nParticipants that had a catch accuracy above 70%:")
print(pplist)
print("\nRemoved participants based on catch accuracy:")
print(remove_participants)

pp_data = np_data
for i in remove_participants:
    pp_data = pp_data[pp_data[:,8]!=i,:]

print('remaining participatnts in pp_data_6080')
print(np.unique(pp_data[:, 8]))

'''delete participants with accuracy lower than 60% or higher than 80%
   - pp_data_6080 contains data for pp with mean_acc part of [60, 80]
   - pp_data contains data for all pp with catch acc > 70%'''
   
Accuracy_trials = pp_data[:, np.array([4, 8])]
Accuracy = [np.mean(Accuracy_trials[Accuracy_trials[:, 1] == i,0])*100 for i in pplist2]

remove_participants_low = pplist2[np.array(Accuracy)<=60]
print('\nRemoved participants due to mean accuracy <= 60')
print(remove_participants_low)
remove_participants_high = pplist2[np.array(Accuracy)>=80]
print('\nRemoved participants due to mean accuracy >= 80')
print(remove_participants_high)

pp_data_6080 = pp_data
for i in remove_participants_low:
    pp_data_6080 = pp_data_6080[pp_data_6080[:,8]!=i,:]
for i in remove_participants_high:
    pp_data_6080 = pp_data_6080[pp_data_6080[:,8]!=i,:]

print('remaining participants in pp_data_6080')
print(np.unique([pp_data_6080[:, 8]]))
print('{} participants remaining in 6080 data'.format(len(np.unique([pp_data_6080[:, 8]]))))

#%%
"""Delete trials where no response was given"""
def delete_no_resp(data = None): 
     no_response = (pp_data[:, 6] == -1)*1
     removed = np.sum(no_response)
     response = no_response == 0
     Clean_Data = pp_data[response,:]
     print("\nThe percentage of trials that were removed because no response was given")
     print((removed/len(data))*100)
     return Clean_Data

pp_data_clean = delete_no_resp(data = pp_data)
pp_data_6080_clean = delete_no_resp(data = pp_data_6080)
    
    
#%%hier verder gaan!!!
"""Rescale RT & Acc
- RT * 1000: for ms
- Acc * 100: for plotting """
def rescale_RT_Acc(data = None): 
    data[:,6]=data[:,6].astype(float)*1000
    data[:,4]=data[:,4].astype(float)*100
    return data

pp_data_clean =  rescale_RT_Acc(data = pp_data_clean)
pp_data_6080_clean = rescale_RT_Acc(data = pp_data_6080_clean)

#%%





"""Export the complete cleaned data-sets for analyses in R 
- for Anova analysis see R """
pp_data_df = pd.DataFrame(pp_data_clean)
pp_data_df.to_csv('pp_data_clean.csv')
pp_data_6080_df = pd.DataFrame(pp_data_6080_clean)
pp_data_6080_df.to_csv('pp_data_6080_clean.csv')

pp_data_df.columns = ['BlockN', 'FTI', 'Flash_position', 'Target_relative_position', 'Accuracy', 'Catch_accuracy', 
                      'RT', 'Block_type', 'Participant nummer', 'FTI_pos']



#%%
"""Convert back to dataframe for easy selection of conditions"""



#%%
def split_FTI(data = None, column_name = 'FTI'): 
    pos_values = np.arange(0, 46, 3)
    neg_values = np.arange(-15, 0, 3)
    pos_FTI = data.loc[data[column_name].isin(pos_values)]
    neg_FTI = data.loc[data[column_name].isin(neg_values)]
    return pos_FTI, neg_FTI


#%% Create the different data per condition (R / nonR; T same / opp; flash L /R)
#split into Reward & non-Reward
def split_Reward(data = None, column_name = 'Block_type'): 
    Rew = data.loc[data[column_name] =='REWARD']
    Non_Rew = data.loc[data[column_name] =='NON REWARD']
    return Rew, Non_Rew

def split_Target_rel(data = None, column_name = 'Target_relative_position'): 
    Same = data.loc[data[column_name] ==0]
    Opp = data.loc[data[column_name] ==1]
    return Same, Opp

def split_Flash(data = None, column_name = 'Flash_position'): 
    Flash_L = data.loc[data[column_name] ==0]
    Flash_R = data.loc[data[column_name] ==1]
    return Flash_L, Flash_R


#%% compute the mean for each FTI & plot the results
def mean_per_FTI(data = None, column_name = 'FTI'):
    n_FTI = len(np.unique(data[column_name]))
    mean_array = np.empty([n_FTI, 3])
    for count, i in enumerate(np.unique(data[column_name])): 
        test = data.loc[data[column_name] ==i]
        mean_array[count, :] = np.array([i, np.mean(test['Accuracy']), np.mean(test['RT'])])
    return mean_array

#%% plot the mean accuracy data
def plot_mean_accuracy(dictionary = None, pp_number = None): 
    fig, axes = plt.subplots(nrows = 4, ncols = 2)
    #fig.set_title('plots for participant {}'.format(pp_number))
    x = 0
    y = 0
    for i in dictionary: 
        axes[x, y].set_title('{}'.format(i))
        axes[x, y].plot(dictionary[i][:, 0].astype(int), dictionary[i][:, 1])
        x += 1
        if x == 4: 
            x = 0
            y = 1
        fig.suptitle('Participant {}'.format(pp_number))
        

#%%
"""Function to do the splitting into conditions all at once"""
def data_to_conditions(this_data = None, FTI = 'pos'): 
    pos_FTI, neg_FTI = split_FTI(data = this_data)
    if FTI == 'pos': 
        this_data = pos_FTI
    else: 
        this_data = neg_FTI
    
    pos_rew, pos_nonrew = split_Reward(data = pos_FTI)
    
    pos_rew_same, pos_rew_opp = split_Target_rel(data = pos_rew)
    pos_nonrew_same, pos_nonrew_opp = split_Target_rel(data = pos_nonrew)
    
    pos_rew_same_flL, pos_rew_same_flR = split_Flash(data = pos_rew_same)
    pos_nonrew_same_flL, pos_nonrew_same_flR = split_Flash(data = pos_nonrew_same)
    pos_rew_opp_flL, pos_rew_opp_flR = split_Flash(data = pos_rew_opp)
    pos_nonrew_opp_flL, pos_nonrew_opp_flR = split_Flash(data = pos_nonrew_opp)
    
    mean_pos_rew_same_flL = mean_per_FTI(data = pos_rew_same_flL)
    mean_pos_rew_same_flR = mean_per_FTI(data = pos_rew_same_flR)
    mean_pos_rew_opp_flL = mean_per_FTI(data = pos_rew_opp_flL)
    mean_pos_rew_opp_flR = mean_per_FTI(data = pos_rew_opp_flR)
    mean_pos_nonrew_same_flL = mean_per_FTI(data = pos_nonrew_same_flL)
    mean_pos_nonrew_same_flR = mean_per_FTI(data = pos_nonrew_same_flR)
    mean_pos_nonrew_opp_flL = mean_per_FTI(data = pos_nonrew_opp_flL)
    mean_pos_nonrew_opp_flR = mean_per_FTI(data = pos_nonrew_opp_flR)
    
    All_conditions = {"R_left_same": mean_pos_rew_same_flL, "R_left_opp": mean_pos_rew_opp_flL,
                      "R_right_same": mean_pos_rew_same_flR, "R_right_opp": mean_pos_rew_opp_flR,
                      "NR_left_same": mean_pos_nonrew_same_flL, "NR_left_opp": mean_pos_nonrew_opp_flL,
                      "NR_right_same": mean_pos_nonrew_same_flR, "NR_right_opp": mean_pos_nonrew_opp_flR}
    
    
    return All_conditions

used_data_df = pp_data_df
used_data_np = pp_data_clean
Conditions_dict = data_to_conditions(this_data = used_data_df, FTI = 'pos')
plot_mean_accuracy(dictionary = Conditions_dict)

for pp in np.unique(used_data_np[:, 8]): 
    single_data_df = pp_data_df.loc[pp_data_df['Participant nummer'] ==pp]
    single_data_np = single_data_df.to_numpy()
    Conditions_dict = data_to_conditions(this_data = single_data_df, FTI = 'pos')
    plot_mean_accuracy(dictionary = Conditions_dict, pp_number = pp)
    


#%%create fourier transform of the data

# def fourier_transform(data = None): 
#     time_points = data[:, 0]*1/60
#     ft = np.fft.fft(data[:, 1])
#     return time_points, ft
# time_points, ft = fourier_transform(data = mean_pos_rew_same_flL)
# average_data = mean_pos_rew_same_flL[:, 1]
# plt.psd(average_data, Fs = 20)


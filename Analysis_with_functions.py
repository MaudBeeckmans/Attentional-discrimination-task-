# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 14:33:30 2021

@author: Maud
"""


#%%Preprocessing part 

import numpy as np
import pandas as pd
import os
import sklearn.linear_model as reg
from scipy import stats
from scipy import signal
from matplotlib import pyplot as plt
import itertools

"""
Laad de data in
Let op voor de volgorde van de datakolommen (zie proefpersoon 4)
"""

pplist = np.arange(1,36)


file_base = os.getcwd() + '\output_files'+'\Outputfile_pp'
print(file_base)

column_names=[]

for i in pplist:

    print("loading data of participant {}".format(i))

    file_name = file_base + str(i) + '.csv'

    if i ==1:
        dat = pd.read_csv(file_name).to_dict('split')
        column_names=dat['columns']
        Data = np.array(dat['data'])
    elif i ==4:
        d = pd.read_csv(file_name).to_numpy()
        d1 = d[:,np.hstack((np.arange(0,19),np.arange(20,35),np.array(19), np.arange(35,40)))]
        Data = np.vstack((Data,d1))
    else:
        Data = np.vstack((Data,pd.read_csv(file_name).to_numpy()))

"""
Bekijk de data eens en selecteer wat je nodig zal hebben
"""

print('\nColumn names of datafile')
print(column_names)

print('\nFirst row of Data')
print(Data[0,:])

Col_to_keep = np.array([0,1,3,5,6,18,20,21,22,26,34,35,36,37,38, 4])
column_names=[column_names[i] for i in Col_to_keep]
Data = Data[:,Col_to_keep]

print('\nThe columns that we keep for analyses')
print(column_names)

print('\nFirst row of data that we kept')
print(Data[0,:])


count = 0
for i in Data[:, 7]: 
    if type(i) != float: 
        if ('f' in i or 'j' in i): 
            Data[count, 7] = float(i[7:-2])
        else: 
            Data[count, 7] = float(i)
    count +=1

#replace pp_number by correct number
Data[:, 14] = Data[:, 14].astype(int)
Data[:, 14] = np.where(Data[:, 14] > 100, Data[:, 14] - 100, Data[:, 14])


"""
Bekijk de accuraatheid in catch trials en verwijder proefpersonen die lager dan 70% scoorden hierop
"""

Catch_trials = Data[~np.isnan(Data[:,10].astype(float)),:]
Catch_trials = Catch_trials[:,np.array([10,14])].astype(float)
Catch_accuracy = [np.mean(Catch_trials[Catch_trials[:,1]==i,0])*100 for i in pplist]

print("\n*****\nAccuracy on catch trials for each participant")
print(Catch_accuracy)

remove_participants = pplist[np.array(Catch_accuracy)<70]
pplist = np.delete(np.array(pplist),remove_participants-1)

print("\nParticipants that had a catch accuracy above 70%:")
print(pplist)
print("\nRemoved participants:")
print(remove_participants)

del_16 = np.unique((pplist == 16), return_index = True)[1][1]
pplist = np.delete(np.array(pplist), del_16)
del_34 = np.unique((pplist == 34), return_index = True)[1][1]
pplist = np.delete(np.array(pplist), del_34)
print(pplist)



pp_data = Data
for i in remove_participants:
    pp_data = pp_data[pp_data[:,14]!=i,:]

"""
Verwijder trials waarin geen response is gegeven
"""

no_response = (pp_data[:,6]==-1)*1
removed = np.sum(no_response)
response = no_response == 0
Clean_Data = pp_data[response,:]

print("\nThe percentage of trials that were removed because no response was given")
print((removed/len(pp_data))*100)

"""
herscoor RT en accuracy:
voor RT doen we *1000 om ms te krijgen
voor accuracy doen we *100 om dat dit duidelijkere plots geeft
"""

Clean_Data[:,7]=Clean_Data[:,7].astype(float)*1000
Clean_Data[:,6]=Clean_Data[:,6].astype(float)*100

"""
Nu bekijken we accuraatheid en RTs over de hele taak maar ook per conditie
we voeren t-tests uit om te kijken of er significante verschillen zijn tussen condities
Accurater zou zijn om een ANOVA te doen met alle 3 de condities (reward, side en before/after flash) in als factoren ipv afzonderlijke t-tests
Nu hou je eigenlijk geen rekening met multiple comparisons en mogelijke interacties tussen factoren
Ik heb nog geen anova gedaan met python en als je maar 3 tests doet is dit ook niet per se erg. Dit is makkelijker :)
"""

pp_accuracy = [np.mean(Clean_Data[Clean_Data[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt = [np.nanmedian(Clean_Data[Clean_Data[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("\n***** \nMean accuracy in general: {:.2f}".format(np.mean(pp_accuracy)))
ci_accuracy = 1.96 * np.std(pp_accuracy, ddof = 1)
print("Accuracy CI95: [{0:.2f} : {1:.2f}]".format(np.mean(pp_accuracy)-ci_accuracy, np.mean(pp_accuracy)+ci_accuracy))
print("Median RT in general: {:.2f}".format(np.mean(pp_rt)))
ci_rt = 1.96 * np.std(pp_rt, ddof = 1)
print("RT CI95: [{0:.2f}:{1:.2f}]  \n********".format(np.mean(pp_rt)-ci_rt, np.mean(pp_rt)+ci_rt))

Before_flash = Clean_Data[:,2].astype(float)<=0
After_flash = Clean_Data[:,2].astype(float)>=0

Data_before=Clean_Data[Before_flash,:]
Data_after=Clean_Data[After_flash,:]

pp_accuracy_before = [np.mean(Data_before[Data_before[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_before = [np.nanmedian(Data_before[Data_before[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("\n***** \nMean accuracy before flash: {}".format(np.mean(pp_accuracy_before)))
print("Median RT before flash: {}".format(np.mean(pp_rt_before)))

pp_accuracy_after = [np.mean(Data_after[Data_after[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_after = [np.nanmedian(Data_after[Data_after[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("Mean accuracy after flash: {}".format(np.mean(pp_accuracy_after)))
print("Median RT after flash: {}".format(np.mean(pp_rt_after)))

Flash_t_accuracy = stats.ttest_rel(pp_accuracy_before, pp_accuracy_after)
Flash_t_rt = stats.ttest_rel(pp_rt_before, pp_rt_after)

print("Flash accuracy t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}".format(Flash_t_accuracy[0], Flash_t_accuracy[1], len(pplist)-1))
print("Flash RT t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}  \n********".format(Flash_t_rt[0], Flash_t_rt[1], len(pplist)-1))

Reward = Clean_Data[:,9]=='REWARD'
No_reward = Clean_Data[:,9]=='NON REWARD'

Data_rew=Clean_Data[Reward,:]
Data_norew=Clean_Data[No_reward,:]

pp_accuracy_rew = [np.mean(Data_rew[Data_rew[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_rew = [np.nanmedian(Data_rew[Data_rew[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("\n***** \nMean accuracy Reward block: {}".format(np.mean(pp_accuracy_rew)))
print("Median RT Reward block: {}".format(np.mean(pp_rt_rew)))

pp_accuracy_norew = [np.mean(Data_norew[Data_norew[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_norew = [np.nanmedian(Data_norew[Data_norew[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("Mean accuracy No reward block: {}".format(np.mean(pp_accuracy_norew)))
print("Median RT No reward block: {}".format(np.mean(pp_rt_norew)))

Reward_t_accuracy = stats.ttest_rel(pp_accuracy_rew, pp_accuracy_norew)
Reward_t_rt = stats.ttest_rel(pp_rt_rew, pp_rt_norew)

print("Reward accuracy t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}".format(Reward_t_accuracy[0], Reward_t_accuracy[1], len(pplist)-1))
print("Reward RT t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}  \n********".format(Reward_t_rt[0], Reward_t_rt[1], len(pplist)-1))

Same_side = Clean_Data[:,3].astype(int)==0
Different_side = Clean_Data[:,3].astype(int)==1

Data_same=Clean_Data[Same_side,:]
Data_diff=Clean_Data[Different_side,:]

pp_accuracy_same = [np.mean(Data_same[Data_same[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_same = [np.nanmedian(Data_same[Data_same[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("\n***** \nMean accuracy Same side: {}".format(np.mean(pp_accuracy_same)))
print("Median RT Same side: {}".format(np.mean(pp_rt_same)))

pp_accuracy_diff = [np.mean(Data_diff[Data_diff[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_diff = [np.nanmedian(Data_diff[Data_diff[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("Mean accuracy Opposite side: {}".format(np.mean(pp_accuracy_diff)))
print("Median RT Opposite side: {}".format(np.mean(pp_rt_diff)))

Side_t_accuracy = stats.ttest_rel(pp_accuracy_same, pp_accuracy_diff)
Side_t_rt = stats.ttest_rel(pp_rt_same, pp_rt_diff)

print("Side accuracy t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}".format(Side_t_accuracy[0], Side_t_accuracy[1], len(pplist)-1))
print("Side RT t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}  \n********".format(Side_t_rt[0], Side_t_rt[1], len(pplist)-1))

Flash_L = Clean_Data[:,15].astype(int)==0
Flash_R = Clean_Data[:,15].astype(int)==1

Data_flL = Clean_Data[Flash_L,:]
Data_flR = Clean_Data[Flash_R,:]

pp_accuracy_flL = [np.mean(Data_flL[Data_flL[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_flL = [np.nanmedian(Data_flL[Data_same[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("\n***** \nMean accuracy flash left: {}".format(np.mean(pp_accuracy_flL)))
print("Median RT flash left: {}".format(np.mean(pp_rt_flL)))

pp_accuracy_flR = [np.mean(Data_flL[Data_flR[:,14].astype(int)==i,6],dtype='float') for i in pplist]
pp_rt_flR = [np.nanmedian(Data_flR[Data_same[:,14].astype(int)==i,7].astype(float)) for i in pplist]

print("Mean accuracy flash right: {}".format(np.mean(pp_accuracy_flR)))
print("Median RT flash right: {}".format(np.mean(pp_rt_flR)))

Flashpos_t_accuracy = stats.ttest_rel(pp_accuracy_flL, pp_accuracy_flR)
Flashpos_t_rt = stats.ttest_rel(pp_rt_flL, pp_rt_flR)

print("Flashpos accuracy t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}".format(Flashpos_t_accuracy[0], Flashpos_t_accuracy[1], len(pplist)-1))
print("Flashpos RT t-value: {0:.4f}, p-value: {1:.4f}, df: {2:d}  \n********".format(Flashpos_t_rt[0], Flashpos_t_rt[1], len(pplist)-1))


#%% Define conditions part & average over FTIs for each condition
print("\n\n\nWe'll extract the data per FTI and per condition")

FTI_list = np.unique(Clean_Data[:,2].astype(float))
Post_list = np.unique(Data_after[:,2].astype(float))
Pre_list = np.unique(Data_before[:,2].astype(float))

Reward_bools = [Reward, No_reward]
Flash_bools = [Flash_L, Flash_R]
Target_bools = [Same_side, Different_side]
    
def extract_conditions(Rew = 1, Fl_pos = 1, T_rel = 1): 
    n_variables = np.sum([Rew, Fl_pos, T_rel])
    n_cond =2**n_variables
    Accuracy_oscillations = np.zeros((len(pplist), len(FTI_list), n_cond))
    conditions_base = np.concatenate([np.repeat(["Rew", "NoRew"], Rew), np.repeat(["L", "R"], Fl_pos), 
                        np.repeat(["same", "opp"], T_rel)]).reshape(n_variables, 2)
    too_much = list(itertools.combinations(np.reshape(conditions_base, (conditions_base.shape[0]*conditions_base.shape[1])), n_variables))
    print(too_much)
    #select = [too_much[np.all(conditions_shape[axis] in too_much) == False] for axis in 
    too_much = np.array(too_much)
    n = 0
    bads = []
    for i in too_much: 
        for axis in range(conditions_base.shape[0]):
            if np.all([conditions_base[axis][0] in i, conditions_base[axis][1] in i]): 
                bads.append(n)   
        n = n+1
    all_conditions = np.delete(too_much, bads, axis = 0)    
    print("All the conditions are listed below")
    print(all_conditions)  
    print("\n******************\n")
    
    
    print("\n***********")
    print("Start the averaging")
    ppid =-1
    for p in pplist:
        ppid +=1
        FTIid =0
        for i in FTI_list:
            condid= 0
            Vari1, Vari2, Vari3 = 0, 0, 0
            for this_cond in all_conditions: 
                if Rew == 1: 
                    Vari1 = Reward_bools[("NoRew" in this_cond)*1]
                if Fl_pos == 1: 
                    Vari2 = Flash_bools[("R" in this_cond)*1]
                if T_rel == 1: 
                    Vari3 = Target_bools[("opp" in this_cond)*1]
                
                id_thiscond = ((Clean_Data[:, 2].astype(float) == i)*1 + (Clean_Data[:,14].astype(int) ==p)*1
                               + Vari1*1*Rew + Vari2*1*Fl_pos + Vari3*1*T_rel) == (n_variables+2)
                Accuracy_oscillations[ppid,FTIid,condid] = np.nanmean(Clean_Data[id_thiscond,6],dtype="float")
                condid += 1
            FTIid +=1
    
    print("Averaging ended")
    return all_conditions, Accuracy_oscillations, n_cond


"""
Nu gaan we de fft doen
Eerst padden we de data om de resolutie te verhogen
je neemt gewoon per conditie en proefpersoon het gemiddelde en gaat die dan voor en achter de data plakken
Ik pad tot we 1 volle seconde aan data hebben met om de 50 ms (3 frames) 1 datapunt
Dat wil zeggen dat we 21 datapunten nodig hebben: van 0 tot 1 in stappen van .05
Voor de 15 FTI's na de flash voeg ik dus 6 punten bij (3 aan elke kant)
Voor de 5 FTI's voor de flash voeg ik 16 punten bij (8 aan elke kant)
"""
"""Aanpassing: 4 & 14 punten bijvoegen, want FTI = 0 ook bij beide (pre & post) opgenomen """


def padding(start_array = None, add_pos_tot = 4, add_neg_tot = 14):
    add_pos = int(add_pos_tot/2)
    add_neg = int(add_neg_tot/2)
    #Padden
    """Moet hier iets aanpassen i.v.m. len(Pre_list) etc. daar moet de 0 ook toegevoegd worden!
        - DONE """
    acc_pad_after = np.reshape(np.tile(np.mean(start_array[:,len(Pre_list)::,:],1),add_pos)
                               ,(len(pplist),add_pos,nConditions))
    Accuracy_padded_after = np.concatenate((acc_pad_after, start_array[:,len(Pre_list)-1::,:], acc_pad_after),axis=1)
    
    acc_pad_before = np.reshape(np.tile(np.mean(start_array[:,0:len(Pre_list),:],1),add_neg),
                                (len(pplist),add_neg,nConditions))
    Accuracy_padded_before = np.concatenate((acc_pad_before, start_array[:,0:len(Pre_list),:], acc_pad_before),axis=1)
    return Accuracy_padded_before, Accuracy_padded_after

step = .05
def FT(Array_of_interest = None, nPermutations = 10000): 
    #FFT, merk op dat ik hier het signaal detrend!
    Power_FFT = np.abs(np.fft.fft(signal.detrend(Array_of_interest,axis=1), axis =1))
    #Bepaal frequenties en extraheer relevante data
    freq_len = np.shape(Power_FFT)[1]
    freqs = np.fft.fftfreq(freq_len, step)
    freq_of_interest = freqs>0
    Power_FFT = Power_FFT[:,freq_of_interest, :]

    print('\n*****\npermutation start')

    """
    Nu doen we de permutatie
    we gaan dus de FTI shufflen en onze FFT telkens opnieuw doen
    """
    
    #Eerst arrays aanmaken om op te slaan
    Power_permutations = np.zeros((len(pplist), freq_len, nConditions, nPermutations))
    freq_id = np.arange(freq_len)
    
    for per in range(nPermutations):
        #shuffle frequenties en doe fft
        np.random.shuffle(freq_id)
        Power_permutations[:,:,:,per] = np.abs(np.fft.fft(Array_of_interest[:,freq_id,:], axis =1))
    
    print('permutation finish\n*****')
    #Hou enkel relevante frequenties
    Power_permutations = Power_permutations[:,freq_of_interest,:,:]
    
    #Bereken Z-score
    Z_power = (Power_FFT - np.mean(Power_permutations, 3))/np.std(Power_permutations, axis = 3, ddof = 1)
    p_threshold = .05/len(freq_of_interest) #bonferoni correctie
    corresponding_Z = 2.575
    Non_corrected_Z = 1.65
    print("\nZ-scores computed, \nsignificance threshold is: {0} \nWhich corresponds to a Z-score of:{1} ".format(p_threshold, corresponding_Z))
    Z_Power_significant = Z_power > corresponding_Z
    print("\n*****\nTested with bonferoni correction for frequencies, {0} subjects on {1} conditions and {2} frequencies: so {3} datapoints in total".format(len(pplist), nConditions, len(freqs), len(pplist)*len(freqs)*nConditions))
    print('For accuracy, {:.0f} datapoints reached significance'.format(np.nansum(Z_Power_significant*1, dtype='float')))
    
    Z_Power_significant_biased = Z_power > Non_corrected_Z
    print("\n*****\nTested without bonferoni correction for frequencies, {0} subjects on {1} conditions and {2} frequencies: so {3} datapoints in total".format(len(pplist), nConditions, len(freqs), len(pplist)*len(freqs)*nConditions))
    print('For accuracy, {:.0f} datapoints reached significance without Bonferroni'.format(np.nansum(Z_Power_significant_biased*1, dtype='float')))
    
    return Z_Power_significant, Z_Power_significant_biased, Power_FFT, Power_permutations

#%%

"""With all the conditions included"""
All_conditions, Accuracy_oscillations2, nConditions = extract_conditions(Rew = 1, Fl_pos = 1, T_rel = 1)

Accuracy_padded_before2, Accuracy_padded_after2 = padding(start_array = Accuracy_oscillations2)

Z_power_sign_after, Z_permutations_sign_after, Power_FFT_after, Power_permutations_after = FT(Array_of_interest = Accuracy_padded_after2)
Z_power_sign_before, Z_permutations_sign_before, Power_FFT_before, Power_permutations_before= FT(Array_of_interest = Accuracy_padded_before2)

#%%
"""Averaged over Reward & Non-Reward"""
All_conditions3, Accuracy_oscillations3, nConditions = extract_conditions(Rew = 0, Fl_pos = 1, T_rel = 1)

Accuracy_padded_before3, Accuracy_padded_after3 = padding(start_array = Accuracy_oscillations3)

Z_power_sign_after3, Z_permutations_sign_after3, Power_FFT_after3, Power_permutations_after3 = FT(Array_of_interest = Accuracy_padded_after3)
Z_power_sign_before4, Z_permutations_sign_before4, Power_FFT_before4, Power_permutations_before4= FT(Array_of_interest = Accuracy_padded_before3)

#%% 


"""Next step: look at the opposite side only: see whether there is over ALL participants a difference in slope!
- thus in fact next step: allow to average over ALL participants (include in function maybe)"""

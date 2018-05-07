import numpy as np
import pandas as pd
#from pandas_datareader import data as wb
import matplotlib.pyplot as plt
from scipy.stats import norm
#%matplotlib inline

input_data = pd.read_csv("data/TimeResourceCost.csv")

NoOfSim = int(input("Kindly enter the no of steps for simulation: "))

data_frame = {}
for i in range(3):
    taskName= input_data.loc[i]['Task']
    time = float(input("Please enter time for " + taskName +" Task: "))
    oTime = float(input("Please enter percentage allowable for overhead time for " + taskName +" Task: "))
    data_frame[taskName] = {'Time':time,
                            'MinFC': time*8,
                            'LikelyFC': time*18*0.8,
                            'MaxFC': time*18,
                            'MinOH': 0.05*time*13,
                            'LikelyOH':(oTime/100)*time*13 * 0.8,
                            'MaxOH':(oTime/100)* time*13
                           }

df_project = pd.DataFrame(data_frame)
df_project = df_project.transpose()


data_frame['Total'] = {     'Time': df_project['Time'].sum(),
                            'MinFC': df_project['MinFC'].sum(),
                            'LikelyFC': df_project['LikelyFC'].sum(),
                            'MaxFC': df_project['MaxFC'].sum(),
                            'MinOH': df_project['MinOH'].sum(),
                            'LikelyOH': df_project['LikelyOH'].sum(),
                            'MaxOH': df_project['MaxOH'].sum()
                        }

df_project = pd.DataFrame(data_frame)
df_project = df_project.transpose()


df_project.reset_index(inplace=True)
df_project['minTC'] = df_project['MinFC'] + df_project['MinOH']
df_project['maxTC'] = df_project['MaxFC'] + df_project['MaxOH']
df_project['LikelyTC'] = df_project['LikelyFC'] + df_project['LikelyOH']
df_project.rename(columns={'index':'Task'}, inplace=True)
#
def pert_random_sample(low, likely, high, samples):
    left = likely - low
    right = high - likely
    leftish = left / (high - low)

    if .4 < leftish < .6:
        a = 3
        b = 3
    elif .2 <= leftish <= .4:
        a = 2
        b = 3
    elif leftish < .2:
        a = 2
        b = 4
    elif .6 <= leftish <= .8:
        a = 3
        b = 2
    elif .8 < leftish:
        a = 4
        b = 2
    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta


sim_result = pd.DataFrame(data=None)
for idx in df_project[:-1].index:
    #print(df_project.iloc[idx])
    minFC = df_project.iloc[idx]['MinFC']
    maxFC = df_project.iloc[idx]['MaxFC']
    likelyFC = df_project.iloc[idx]['LikelyFC']

    minOH = df_project.iloc[idx]['MinOH']
    maxOH = df_project.iloc[idx]['MaxOH']
    likelyOH = df_project.iloc[idx]['LikelyOH']

    minTC = df_project.iloc[idx]['minTC']
    maxTC = df_project.iloc[idx]['maxTC']
    LikelyTC = df_project.iloc[idx]['LikelyTC']

    task = df_project.iloc[idx]['Task']
    colname_TC = task + ' Total Cost'
    colname_VC = task + ' Variable Cost'
    colname_FC = task + ' Fixed Cost'


    list_FC = []
    list_VC = []
    list_TC = []

    for i in range(NoOfSim):
        #randVal = pert_random_sample(minFC,likelyFC, maxFC,1)
        list_FC.append(pert_random_sample(minFC,likelyFC, maxFC,1)[0])
        list_VC.append(pert_random_sample(minOH,likelyOH, maxOH,1)[0])
        list_TC.append(pert_random_sample(minTC,LikelyTC, maxTC,1)[0])

    sim_result[colname_FC] = list_FC
    sim_result[colname_VC] = list_VC
    sim_result[colname_TC] = list_TC

project_cost = []

minTC = df_project[-1:]['minTC'].values[0]
maxTC = df_project[-1:]['maxTC'].values[0]
LikelyTC = df_project[-1:]['LikelyTC'].values[0]

print(minTC, LikelyTC, maxTC)
for i in range(NoOfSim):
    #randVal = pert_random_sample(minFC,likelyFC, maxFC,1)
    project_cost.append(pert_random_sample(minTC,LikelyTC, maxTC,1)[0])

sim_result['Project Cost'] = project_cost

labels= ["Design","Development", "Test"]
for i in df_project[:-1].index:
    col_name= df_project.loc[i]["Task"] + " Total Cost"
    plt.hist(sim_result[col_name], bins=100)
    plt.xlabel(col_name)
    plt.ylabel('Frequency')
    #plt.legend(labels)
    plt.title('Histogram of ' + col_name)
    plt.show()

task_est_cost = []
for idx in df_project[:-1].index:
    task = df_project.loc[idx]['Task']
    col_name = task + ' Total Cost'
    task_est_cost.append(np.mean(sim_result[col_name]))

task_est_cost.append(np.mean(sim_result['Project Cost']))
df_project['Estimated Cost'] = task_est_cost

print(" -" * 25)
print(df_project[:-1][["Task",  "LikelyTC" , "Estimated Cost"]])
print(" -" * 25)


print(" -" * 25)
print("PROJECT LIKELY COST   |    PROJECT ESTIMATED COST.")
print(" -" * 25)
print( str(df_project[-1:]["LikelyTC"].values[0])+ " " *25 + str(np.mean(sim_result['Project Cost'])))
print(" -" * 25)

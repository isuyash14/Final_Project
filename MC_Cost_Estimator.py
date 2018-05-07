import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
from scipy.stats import norm

### Read Data File

df_project = pd.read_csv("../data/Resource Cost.csv")
df_project['minTC'] = df_project['MinFC'] + df_project['MinOH']
df_project['maxTC'] = df_project['MaxFC'] + df_project['MaxOH']
df_project['LikelyTC'] = df_project['LikelyFC'] + df_project['LikelyOH']


### Function for getting random samepl from Pert distribution

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

#### Function for assigning labels to the plot
###

def get_label(x):

    if x < 252:
        val = 200
    elif 252 < x < 302:
        val = 250
    elif 302 <= x < 350:
        val = 300
    elif 352 <= x < 402:
        val = 350
    elif 402 <= x < 452:
        val = 400
    elif 452 <= x < 502:
        val = 450
    elif 502 <= x < 552:
        val = 500
    elif 552 <= x < 602:
        val = 550
    elif 602 <= x < 652:
        val = 600
    elif 652 <= x < 702:
        val = 650
    elif 702 <= x < 752:
        val = 700
    else:
        val = 800

    return val

## Function for performing N Simulations
## This function returns a DataFrame for the simulation results.

def do_simulations(No_Of_Sim):
    sim_result = pd.DataFrame(data=None)
    for idx in df_project[:-1].index:
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

        for i in range(No_Of_Sim):
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
    for i in range(No_Of_Sim):
        #randVal = pert_random_sample(minFC,likelyFC, maxFC,1)
        project_cost.append(pert_random_sample(minTC,LikelyTC, maxTC,1)[0])

    sim_result['Project Cost'] = project_cost
    return sim_result

sim_result = do_simulations(100)
plt.hist(sim_result['Project Cost'])
plt.xlabel('Project Cost.')
plt.ylabel('Frequency')
plt.title('Histogram of Project Cost')
#plt.show()

task_est_cost = []
for idx in df_project[:-1].index:
    task = df_project.loc[idx]['Task']
    col_name = task + ' Total Cost'
    task_est_cost.append(np.mean(sim_result[col_name]))


task_est_cost.append(np.mean(sim_result['Project Cost']))
df_project['Estimated Cost'] = task_est_cost

print(" -" * 25)
print("PROJECT LIKELY COST   |    PROJECT ESTIMATED COST.")
print(" -" * 25)
print( str(df_project[-1:]["LikelyTC"].values[0])+ " " *25 + str(np.mean(sim_result['Project Cost'])))
print(" -" * 25)

print(" TASK    |   LIKELY COST |   ESTIMATED COST.")
print(" -" * 25)
for i in df_project[:-1].index:
    task_name = df_project.loc[i]['Task']
    print(task_name + "     " + str(df_project.loc[i]["LikelyTC"])+ "   " + str(np.mean(sim_result['Test Total Cost'])))

print(df_project[:-1][["Task",  "LikelyTC" , "Estimated Cost"]])
print(" -" * 25)

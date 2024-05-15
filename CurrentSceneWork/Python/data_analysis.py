import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import glob
import os

def summarize_sensor_trace(csv_file: str):
    '''
    Gets the mean and variance for a given data file
    
    Returns: Dataframe with means and variances for file
    '''
    if str(os.getcwd()).find("Data\Lab1") < 0 :
        os.chdir("../Data/Lab1/")
    #os.listdir()
    mydata = pd.read_csv(csv_file, index_col=False)
    #print(mydata)
    mysumdata = mydata.describe().reset_index()
    #print(mydata.describe())
    mysumref = pd.DataFrame(columns=['mean', 'variance'], index=mysumdata.columns)
    #print(mysumref.columns)
    #print(mysumref.index)
    #print(mysumdata.iloc[1, 1:])
    mysumref['mean'] = mysumdata.iloc[1, 1:]
    mysumref['variance'] = mysumdata.iloc[2, 1:] ** 2
    mysumref = mysumref.drop(['index'])
    #print(mysumref)
    #mysumref.to_csv(csv_file[:-4] + "summarystats.csv")
    return mysumref, len(mysumdata), mysumref.index
    
    #print("TEST")
def visualize_sensor_trace(csv_file: str, attribute: str):
    '''
    Plots the graphs to visualize data for a given file and attribute
    '''
    #print(os.listdir(path='../Data/Lab1'))
    #print(str(os.listdir()))
    #print(os.getcwd())
    if str(os.getcwd()).find("Data\Lab1") < 0 :
        os.chdir("../Data/Lab1/")
            
    mydata = pd.read_csv(csv_file, index_col=False)
    #print(mydata.head(5))
    
    dims = ['x', 'y', 'z']
    units = [('vel', "m/s"), ('angularVel', "rad/s"), ('pos', 'm'), ('rot', "degrees")]
    #print(attribute)
    for i in dims:
        attselect = attribute + "." + i
        #print(attselect)
        plt.plot(mydata['time'], mydata[attselect], label=attselect+"_"+csv_file[:-4])
        
    
    plt.xlabel("Time (ms)")
    chosenunit = ""
    for j in units:
        if attribute == j[0]:
            chosenunit = j[1]

    plt.ylabel(attribute + " (x,y,z) in " + chosenunit)
    
    myfig = plt.gcf()
    return myfig
    #os.chdir("../../Python")
    #plt.savefig(csv_file[:-4]+attribute+"graph.png")
    
    #plt.savefig(attribute + "(x,y,z)" + '.png')


#summarize_sensor_trace("ARC_02.csv")
#visualize_sensor_trace("ARC_02.csv", "headset_vel")

def kinetic_energy(mass, velocity):
    '''
    Calculates the kinetic energy for a given mass and velocity
    NOT TO BE USED IN ANALYSIS, I HAD THIS ORIGINALLY, BUT DUE TO THE SCOPE OF THE
    ASSIGNMENT I HAVE CHOSEN TO NOT UTILIZE THIS FUNCTION AND ITS ASSOCIATED STATISTICS AND VISUALS
    
    Returns: A vector of kinetic energies for the velocities for a given mass
    '''
    #quest2 + hand ~ 547g = 0.547 kg
    #I weigh 63.5029 kg
    #head + headset = 5.503 kg
    
    myarr = 1/2 * mass * velocity**2
    return myarr

def acceleration(velocity, time):
    '''
    Calculates the acceleration given the provided times and velocities
    
    Returns: A vector of accelerations over  time intervals
    
    '''
    acc_list = []
    delta_time = []
    for i in range(len(velocity) - 1):
        acc_list.append((velocity[i+1] + velocity[i]) / (time[i+1] - time[i]))
        delta_time.append((time[i+1] - time[i]))
    return acc_list, delta_time


    

def visualize_multiple_sensor_traces(files, attribute):
    '''
    Utilizes similar code to visual_sensor_traces to print out multiple
    graphs of time series for sensor data for given activities for a given
    attribute
    
    '''
    #print(os.listdir(path='../Data/Lab1'))
    #print(str(os.listdir()))
    #print(os.getcwd())
    fig, ax = plt.subplots(7, figsize=(10, 10))
    fig.tight_layout(pad=5)
 

    
    incre = 0
    for file in files:
        if str(os.getcwd()).find("Data\Lab1") < 0 :
            os.chdir("../Data/Lab1/")
                
        mydata = pd.read_csv(file, index_col=False)
        #print(mydata.head(5))

        dims = ['x', 'y', 'z']
        units = [('vel', "m/s"), ('angularVel', "rad/s"), ('pos', 'm'), ('rot', "degrees")]
        #print(attribute)
        
        for i in dims:
            
            attselect = attribute + "." + i
            #print(attselect)
            
            chosenunit = ""
            for j in units:
                if attribute[attribute.rfind("_")+1:] == j[0]:
                    chosenunit = j[1]
                    
            ax[incre].plot(mydata['time'], mydata[attselect], label=attselect+"_"+file[:-4])
            ax[incre].title.set_text(file + " " + attribute + " " + chosenunit)
            if incre == 7:
                ax[incre].set_xlabel("Time (ms)")
            
            
            #print(attribute[attribute.rfind("_")+1:])
            
            #ax[incre].set_ylabel(attribute[attribute.rfind("_")+1:] + " " + chosenunit)
        
        
        incre+=1
        
        
    plt.show()
    fig.savefig(attribute+"_plot.png")



def getdata_from_data():
    '''
    Gets the summary data and visual data for all of the activity data. The summary data for each of the
    activities is printed and saved in a csv file in the same directory. The image plots of the data (containing
    x, y, and z values) are stored in the same director. This process is also repeated for kinetic energy.
    Summary statistics and graphs for the all features and important features are all stored in the Data folder.
    
    NOTE: DO NOT RUN THIS METHOD UNTIL YOU WISH TO SEE THE DATA COLLECTED AND STORED
    I account for this by ignoring previously generated csvs in my data configuration, but note the size of the Data/Lab1
    folder will change to hold these files
    
    '''
    
    
    filelist = list(os.listdir(path='../Data/Lab1'))
    #print(filelist)
    #print(len(filelist))
    activlist = ['ARC', 'SIT', 'JOG', 'STD', 'STR', 'TWS', 'DRI']
    grabinds = []
    combfiles = []
    candidate_att_check = ['controller_left_vel',
        'controller_left_angularVel', 'controller_left_pos',
        'controller_left_rot', 'controller_right_vel',
        'controller_right_angularVel', 'controller_right_pos',
        'controller_right_rot', 'headset_pos']

    mynames = []
    for act in activlist:
        myacts = [i for i in filelist if i.find(act) >= 0 and i.find("COMBINED") < 0 and i.find("SUMMARY") < 0]
        #print(myacts)
        actdatastore = pd.DataFrame(columns=['mean', 'variance'])
        mydatastore, numpoints, grabinds = summarize_sensor_trace(myacts[0])
        mygetdata = pd.read_csv(myacts[0], index_col=False).reset_index()
        #print("CHECK RECEIVE DATA:", mygetdata.head(5))
        combined_data_pls = pd.DataFrame()
        #print(combined_data_pls)
        combined_data_pls = pd.concat([combined_data_pls, mygetdata.head(730)])
        #print("COMB DATA PLS:\n", combined_data_pls)
        actdatastore = pd.concat([actdatastore, mydatastore])
        

        
        
        for data in myacts[1:]:
            mydatastore, numpoints, grabinds = summarize_sensor_trace(data)
            actdatastore['mean'] = actdatastore['mean'] + mydatastore['mean']
            actdatastore['variance'] = actdatastore['variance'] + mydatastore['variance']
            combined_data_pls = (combined_data_pls + pd.read_csv(data, index_col=False).reset_index().head(730))/2
            #print(combined_data_pls)
        
        
        actdatastore['mean'] = actdatastore['mean'] / 7
        actdatastore['variance'] = actdatastore['variance'] / 7
        #os.chdir("../../Python")S
        #print(combined_data_pls.head(5))
        #print(actdatastore.reset_index().index)
        mymask = actdatastore.reset_index().index.isin([0,8,9,10,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])
        myactdata = actdatastore.reset_index()[mymask]
        
        
        #print(myactdata)
        #.loc[[0,8,9,10,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]]
        myactdata.to_csv("SUMMARY_"+act+".csv")
        actdatastore.to_csv("SUMMARY_ALL_STATS_"+act+".csv")
        
        combined_data_pls.to_csv("COMBINED_"+act+".csv")
        mynames.append("COMBINED_"+act+".csv")
        #print(mynames)
        #print(actdatastore)
        
    
    for myact_choice in mynames:
        myaccdata = pd.read_csv(myact_choice)
        accdf = pd.DataFrame()
        myaccdatavel = myaccdata[['time', 'headset_vel.x', 'headset_vel.y', 'headset_vel.z', 'controller_left_vel.x', 'controller_left_vel.y', 'controller_left_vel.z',\
        'controller_right_vel.x', 'controller_right_vel.y', 'controller_right_vel.z']]
        
        nada = []
        for velcol in list(myaccdatavel.columns)[1:]:
            if velcol.find("headset") >= 0:
                accdf[velcol[:-5]+"acceleration."+velcol[-1:]], nada= acceleration(myaccdatavel[velcol], myaccdatavel['time'])
            else:
                accdf[velcol[:-5]+"acceleration."+velcol[-1:]], nada = acceleration(myaccdatavel[velcol], myaccdatavel['time'])
        print(accdf.head(5))
        accdf.describe().reset_index().to_csv("ACCELDF_"+myact_choice+".csv")
        
        
        fig3, ax3 = plt.subplots(9, figsize=(10, 10))
        fig3.tight_layout(pad=4)
        incre3 = 0
        mycollist = list(accdf.columns)
        print(mycollist)
        print(mycollist)
        print(len(mycollist))
        for energycol in mycollist:
            print(incre3)
            print(ax3[0])
            ax3[incre3].plot(accdf.index.values.tolist(), accdf[energycol], label=energycol+"_"+myact_choice[:-4])
            ax3[incre3].title.set_text(myact_choice + " " + energycol + " (kg*(m/s)^2)")
            if incre3== 8:
                ax3[incre3].set_xlabel("Time (ms)")
            incre3+=1
            
        plt.show()
        fig3.savefig(myact_choice[:-4]+"_acceleration_plot.png")
        
        
    #I also calculate the kinetic energy for myself, but did not include it in my report as it
    #require data outside of the raw data
    for myact_choice in mynames:
        my_kin_data = pd.read_csv(myact_choice)
        myenergy_df = pd.DataFrame()
        my_kin_data_vel = my_kin_data[['time', 'headset_vel.x', 'headset_vel.y', 'headset_vel.z', 'controller_left_vel.x', 'controller_left_vel.y', 'controller_left_vel.z',\
        'controller_right_vel.x', 'controller_right_vel.y', 'controller_right_vel.z']]
        
        for velcol in list(my_kin_data_vel.columns)[1:]:
            if velcol.find("headset") >= 0:
                myenergy_df[velcol[:-5]+"kin_energy."+velcol[-1:]] = kinetic_energy(0.547, my_kin_data_vel[velcol])
                #weight of hand + controller in kg
            else:
                myenergy_df[velcol[:-5]+"kin_energy."+velcol[-1:]] = kinetic_energy(5.503, my_kin_data_vel[velcol])
                #weight of head + headset in kg
                
    
        myenergy_df.describe().reset_index().to_csv("ENERGYDF_"+myact_choice+".csv")
        fig2, ax2 = plt.subplots(9, figsize=(10, 10))
        fig2.tight_layout(pad=4)
        incre2 = 0
        
        
        for energycol in myenergy_df.columns:
            ax2[incre2].plot(my_kin_data_vel['time'], myenergy_df[energycol], label=energycol+"_"+myact_choice[:-4])
            ax2[incre2].title.set_text(myact_choice + " " + energycol + " (kg*(m/s)^2)")
            if incre2 == 8:
                ax2[incre2].set_xlabel("Time (ms)")
            incre2+=1
        plt.show()
        fig2.savefig(myact_choice[:-4]+"_kinenergy_plot.png")
        
        
    
        
        
    for cand in candidate_att_check:
        visualize_multiple_sensor_traces(mynames, cand)
        
    
    
    
        
        
        
        
        
        
            
            
            
        
        
    #print(grabinds)
    

getdata_from_data()


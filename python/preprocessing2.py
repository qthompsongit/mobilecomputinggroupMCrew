import argparse
from glob import glob
import os
import pickle

import pandas as pd
import numpy as np
import json
import os
import glob
import shutil
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix, classification_report
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
import time
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier

#The code below is the same as preprocessing.py but removes refereneces to semi-erratic movement
def getfiles_makedata():
    print(os.getcwd())
    os.chdir("dataformodel")
    #print(os.listdir())
    ar_str_dr = ["Quinn", "Ksennia", "Ilana"]
    dr_sit_tws = ["Urunna"]
    str_jog_arc = ["Josh"]
    myfeats = ["time", "headset_vel.x", "headset_vel.y", "headset_vel.z",\
    "headset_angularVel.x", "headset_angularVel.y", "headset_angularVel.z",\
    "headset_pos.x", "headset_pos.y", "headset_pos.z",\
    "headset_rot.x", "headset_rot.y", "headset_rot.z",\
    "controller_left_vel.x", "controller_left_vel.y", "controller_left_vel.z",\
    "controller_left_angularVel.x", "controller_left_angularVel.y", "controller_left_angularVel.z",\
    "controller_left_pos.x", "controller_left_pos.y", "controller_left_pos.z",\
    "controller_left_rot.x", "controller_left_rot.y", "controller_left_rot.z",\
    "controller_right_vel.x", "controller_right_vel.y", "controller_right_vel.z",\
    "controller_right_angularVel.x", "controller_right_angularVel.y", "controller_right_angularVel.z",\
    "controller_right_pos.x", "controller_right_pos.y", "controller_right_pos.z",\
    "controller_right_rot.x", "controller_right_rot.y", "controller_right_rot.z", "breathread"]
    
    mydfdata_train = pd.DataFrame(columns=myfeats)
    mydfdata_test = pd.DataFrame(columns=myfeats)
    #print(mydfdata.columns)
    incre = 0 
    
    #build the training and test datasets from provided files
    for name in ar_str_dr:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        print(file_list)
        for file in file_list:
            readfile = pd.read_csv(file, index_col=False)
            if file.find("ARC") >= 0:
                readfile['breathread'] = 'normal'
            if file.find("STR") >= 0:
                readfile['breathread'] = 'erratic'
            if file.find("DRI") >= 0:
                readfile['breathread'] = 'erratic'
            #print(readfile.head(5))
            #print(readfile.columns)
            if incre > 3:
                mydfdata_train = pd.concat([mydfdata_train, readfile])
            else :
                mydfdata_test = pd.concat([mydfdata_test, readfile])
            incre+=1
        
        incre = 0
        os.chdir("..")
    #print(mydfdata_train.isnull())
    
    for name in dr_sit_tws:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        print("FILES FOR", name, file_list)
        for file in file_list:
            readfile = pd.read_csv(file, index_col=False)
            if file.find("DRI") >= 0:
                readfile['breathread'] = 'normal'
            if file.find("SIT") >= 0:
                readfile['breathread'] = 'erratic'
            if file.find("TWS") >= 0:
                readfile['breathread'] = 'erratic'
            #print(readfile.head(5))
            #print(readfile.columns)
            if incre > 3:
                mydfdata_train = pd.concat([mydfdata_train, readfile])
            else :
                mydfdata_test = pd.concat([mydfdata_test, readfile])
            incre+=1
        
        incre = 0
        os.chdir("..")
    #print(mydfdata_test.isnull())
    for name in str_jog_arc:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        print("FILES FOR", name, file_list)
        for file in file_list:
            readfile = pd.read_csv(file, index_col=False)
            if file.find("STR") >= 0:
                readfile['breathread'] = 'normal'
            if file.find("JOG") >= 0:
                readfile['breathread'] = 'erratic'
            if file.find("ARC") >= 0:
                readfile['breathread'] = 'erratic'
            #print(readfile.head(5))
            #print(readfile.columns)
            if incre > 3:
                mydfdata_train = pd.concat([mydfdata_train, readfile])
            else :
                mydfdata_test = pd.concat([mydfdata_test, readfile])
            incre+=1
        
        incre = 0
        os.chdir("..")
        
        
    #save to files     
    mydfdata_test.to_csv("test_data_2.csv")
    mydfdata_train.to_csv("train_data_2.csv")
    
    return mydfdata_train, mydfdata_test
  
#train the models on loaded data    
def train_model(train_data):
    myclasscheck = MLPClassifier(hidden_layer_sizes=100, learning_rate="adaptive", max_iter=1000)
    myrandforcheck = RandomForestClassifier(n_estimators=100, max_depth = 10)
    train_data = train_data.dropna()
    myfeats = train_data[train_data.columns[:-1]]
    mypred = train_data[train_data.columns[-1]]
    
    myclasscheck.fit(myfeats, mypred)
    myrandforcheck.fit(myfeats, mypred)
    predcheck = myrandforcheck.predict(myfeats)
    predcheck2 = myclasscheck.predict(myfeats)
    print("RANDOM FOREST:", classification_report(mypred, predcheck))
    print("MLP:", classification_report(mypred, predcheck2))
    return myrandforcheck, myclasscheck
    
#evaluate the models on a test set
def evaluate_model(model, tester_data):
    myfeats = tester_data[tester_data.columns[:-1]]
    mypred = tester_data[tester_data.columns[-1]]
    mypredcheck = model.predict(myfeats)
    print(classification_report(mypred, mypredcheck))
    
#save models to be used later    
train_data, test_data = getfiles_makedata()
testmodelrandfor, testmodelmlp = train_model(train_data)
print("RANDOM FOREST TEST")
evaluate_model(testmodelrandfor, test_data)
print("MLP TEST")
evaluate_model(testmodelmlp, test_data)

fp = open("../mymodelfile_randfor_2","wb") 
pickle.dump(testmodelrandfor, fp) 
fp.close()

fp = open("../mymodelfile_mlp_2","wb") 
pickle.dump(testmodelmlp, fp) 
fp.close()
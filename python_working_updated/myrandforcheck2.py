import os
import pickle
import sys

import pandas as pd
import numpy as np
import json
import os
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix, classification_report
from collections import Counter
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import time
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

def getfiles_makedata():
    #print(os.getcwd())
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
    #assign breahting level classifications
    for name in ar_str_dr:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        #print(file_list)
        for file in file_list:
            readfile = pd.read_csv(file, index_col=False)
            if file.find("ARC") >= 0:
                readfile['breathread'] = 'normal'
            if file.find("STR") >= 0:
                readfile['breathread'] = 'semi-erratic'
            if file.find("DRI") >= 0:
                readfile['breathread'] = 'erratic'
            #print(readfile.head(5))
            #print(readfile.columns)
            mydfdata_train = pd.concat([mydfdata_train, readfile])        
        incre = 0
        os.chdir("..")
    #print(mydfdata_train.isnull())
    
    for name in dr_sit_tws:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        #print("FILES FOR", name, file_list)
        for file in file_list:
            readfile = pd.read_csv(file, index_col=False)
            if file.find("DRI") >= 0:
                readfile['breathread'] = 'normal'
            if file.find("SIT") >= 0:
                readfile['breathread'] = 'semi-erratic'
            if file.find("TWS") >= 0:
                readfile['breathread'] = 'erratic'
            #print(readfile.head(5))
            #print(readfile.columns)
            mydfdata_train = pd.concat([mydfdata_train, readfile])

        
        incre = 0
        os.chdir("..")
    #print(mydfdata_test.isnull())
    #repeat build sets one last time
    for name in str_jog_arc:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        #print("FILES FOR", name, file_list)
        for file in file_list:
            readfile = pd.read_csv(file, index_col=False)
            if file.find("STR") >= 0:
                readfile['breathread'] = 'normal'
            if file.find("JOG") >= 0:
                readfile['breathread'] = 'semi-erratic'
            if file.find("ARC") >= 0:
                readfile['breathread'] = 'erratic'
            #print(readfile.head(5))
            #print(readfile.columns)
            mydfdata_train = pd.concat([mydfdata_train, readfile])
        
        incre = 0
        os.chdir("..")
        
        
    mydfdata_train = mydfdata_train.dropna()
    #repeat for different sets of data
    
    mytrain_X, mytest_X, mytrain_y, mytest_y = train_test_split(mydfdata_train.drop(columns=['breathread']), mydfdata_train['breathread'])
    #print(mytrain_X.shape)
    
    return mytrain_X, mytest_X, mytrain_y, mytest_y
        
#train the model with the provided data
def train_model(train_data_X, train_data_y):
    #myclasscheck = MLPClassifier(hidden_layer_sizes=1000, learning_rate="adaptive", max_iter=1000)
    myrandforcheck = RandomForestClassifier(n_estimators=100, max_depth = 10)
    #train_data = train_data.dropna()
    myfeats = train_data_X
    mypred = train_data_y
    
    #myclasscheck.fit(myfeats, mypred)
    myrandforcheck.fit(myfeats, mypred)
    predcheck = myrandforcheck.predict(myfeats)
    #predcheck2 = myclasscheck.predict(myfeats)
    #print("RANDOM FOREST:", classification_report(mypred, predcheck))
    #print("MLP:", classification_report(mypred, predcheck2))
    return myrandforcheck
    
#evaluate the model with classification report
def evaluate_model(model, mytest_X, mytest_y):
    myfeats = mytest_X
    mypred = mytest_y
    mypredcheck = model.predict(myfeats)
    print(classification_report(mypred, mypredcheck))


def makepred(mymod, mytestdata):
    #run predict probability and take the most common reading
    myprediction = mymod.predict_proba(mytestdata)
    #print(mymod.classes_)
    arrcheck = [0, 0, 0]
    predict_val = ['erratic', 'normal', 'semi-erratic']
    for stats in myprediction:
        arrcheck[list(stats).index(max(stats))] += 1
    #print(myprediction)
    #print(arrcheck)
    return predict_val[arrcheck.index(max(arrcheck))]
        


if __name__ == '__main__':
    #print("MY ARGS:", list(sys.argv))
    with open('somefile.txt', 'a') as the_file:
        the_file.write(list(sys.argv)[1])
    #print("COMPLETE CHECKS")
    #print(sys.argv[1])
    mytrain_X, mytest_X, mytrain_y, mytest_y = getfiles_makedata()
    testmodelrandfor = None
    os.chdir("..")
    #print(os.listdir())
    if "testrandfor" not in os.listdir() :
        #mytrain_X, mytest_X, mytrain_y, mytest_y = getfiles_makedata()
        testmodelrandfor = train_model(mytrain_X, mytrain_y)
        #print(os.listdir())
        os.chdir("..")
        fp = open("testrandfor","wb") 
        pickle.dump(testmodelrandfor, fp) 
        fp.close()
    else :
        fp = open("testrandfor","rb")
        testmodelrandfor = pickle.load(fp)
        fp.close()
    print("RANDOM FOREST TEST")
    evaluate_model(testmodelrandfor, mytest_X, mytest_y)
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
    "controller_right_rot.x", "controller_right_rot.y", "controller_right_rot.z"]
    
    mydfdata_train = pd.read_csv(list(sys.argv)[1], index_col=False)
    mydfdata_train['breathread'] = 'normal'
    #print("NUM FEATS:", len(myfeats))
    #print("NUM FEATS2:", len(list(sys.argv)[1].split(",")))
    
    #mydfdata_train.loc[len(mydfdata_train)] = list(sys.argv)[1].split(",")[:-1]
    
    #print(mydfdata_train.head())
    
    #print(testmodelrandfor.classes_)
    myguesses = ['erratic', 'normal', 'semi-erratic']
    result = testmodelrandfor.predict(mydfdata_train.drop(columns=['breathread']))
    
    mytestcheck = pd.read_csv("test_data.csv", index_col=0).dropna()
    #print("CHECK ON TEST AGAIN:")
    #evaluate_model(testmodelrandfor, mytestcheck.drop(columns=['breathread']), mytestcheck['breathread'])
    #print("CHECK ON NEW STUFF AGAIN:")
    #evaluate_model(testmodelrandfor, mydfdata_train.drop(columns=['breathread']), mydfdata_train['breathread'])
    print(result[0])
    #print(list(sys.argv)[1])
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


def getfiles_makedata():
    print(os.getcwd())
    os.chdir("dataformodel")
    #print(os.listdir())
    ar_str_dr = ["Quinn", "Ksennia", "Ilana"]
    dr_sit_tws = ["Urunna", "Josh"]
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
    
    mydfdata = pd.DataFrame(columns=myfeats)
    #print(mydfdata.columns)
    for name in ar_str_dr:
        os.chdir(name)
        file_list = [i for i in os.listdir() if i.find("info") < 0]
        print(file_list)
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
            mydfdata = pd.concat([mydfdata, readfile])
        os.chdir("..")
        
    print(mydfdata.shape)
    print(mydfdata.head(5))
        
    
    
def train_test_split():
    print(os.getcwd())
    
getfiles_makedata()
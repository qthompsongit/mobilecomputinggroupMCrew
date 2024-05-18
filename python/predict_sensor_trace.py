import sys
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
import energyusage

def makepred(n = 10):
    fp = open("mymodelfile_randfor_2","rb") 
    myrandfor = pickle.load(fp) 
    fp.close()
    mydataset = pd.read_csv(sys.argv[1], index_col=False)
    print(mydataset.head(5))
    myprediction = myrandfor.predict_proba(mydataset)
    print(myrandfor.classes_)
    arrcheck = [0, 0, 0]
    predict_val = ['erratic', 'normal', 'semi-erratic']
    for stats in myprediction:
        arrcheck[list(stats).index(max(stats))] += 1
    print(myprediction)
    print(arrcheck)

    with open("myprediction.txt", "w") as myfile:
        myfile.write(predict_val[arrcheck.index(max(arrcheck))])
        
#energyusage.evaluate(makepred, 10, pdf=False, printToScreen=True)


# user function to be evaluated
def recursive_fib(n):
    if (n <= 2): return 1
    else: return recursive_fib(n-1) + recursive_fib(n-2)

energyusage.evaluate(recursive_fib, 40, pdf=True)
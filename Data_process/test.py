# -*- coding: UTF-8 –*-
import  pandas as pd
import Utils.PathUtils as pu
import matplotlib
import  matplotlib.pyplot as plt
import  Utils.FeatureUtil as fu
import pickle
import multiprocessing
import numpy as np
from multiprocessing import  Pool
import Utils.FeatureUtil as fu
import os
pd.set_option("display.max_columns",5000)
pd.set_option("display.max_rows",5000)
pd.set_option("display.width",1000)
pd.set_option("display.max_colwidth",100)

# rootdir =r"C:\Users\Tobin\Downloads"
# filenams =os.listdir(rootdir)
# id = pd.read_csv(r"C:\Users\Tobin\Downloads\12aa3442-2365-4fb9-a161-7e8ba5a30100.csv")[["id"]]
# res =id
# for item in filenams:
#     path = os.path.join(rootdir,item)
#     if ".csv" in path:
#        res = pd.concat([res, pd.read_csv(path)[["predicition"]]], axis=1)
#
#
# features = list(res.columns)
# features.remove("id")
# mean = pd.DataFrame(res[features].mean(1), columns=["predicition"])
# res = pd.concat([id, mean], axis=1)
# print(res)
# res.to_csv(pu.predict_rootpath + "yy.csv", index=None)




id = pd.read_csv(pu.predict_rootpath +"yy.csv")["id"]
other = pd.read_csv(pu.predict_rootpath +"qq.csv")["predicition"]
best = pd.read_csv(pu.predict_rootpath +"aa.csv")["predicition"]
label = (other*0.4+best*0.6)
res = pd.DataFrame(pd.concat([id,label],axis=1),columns=["id","predicition"])
res.to_csv(pu.predict_rootpath + "final.csv", index=None)
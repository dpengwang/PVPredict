import Utils.PathUtils as pu
import pandas as pd
import matplotlib
import  matplotlib.pyplot as plt


def remove_exception_data(origin_data):

    data = pd.DataFrame(origin_data[["时间","实际功率"]])
    data["时间"] = data["时间"].apply(lambda x: x.split(" ")[0])

    res = data["实际功率"].groupby(data["时间"]).sum()
    res = pd.DataFrame(res).reset_index()

    y = res[["实际功率"]].iloc[:,0].values
    x = res[["时间"]].iloc[:,0].values

    mean = sum(list(y))/len(y)
    high = int(mean * 1.6)
    low  = int(mean * 0.3)
    badtime = []

    for i in range(len(y)):
        if int(y[i]) not in range(low,high):
             badtime.append(x[i])
    origin_data = origin_data[origin_data["时间"].apply(lambda x:x.split(" ")[0] not in badtime)]
    return origin_data

data = pd.read_csv(pu.train4_path)
print(remove_exception_data(data))
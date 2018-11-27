# -*- coding: UTF-8 –*-
import matplotlib
import Utils.PathUtils as pu
import  matplotlib.pyplot as plt
import math
import  pandas as pd
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
matplotlib.use('qt4agg')

path = "C:/Users/Tobin/PycharmProjects/PhotovoltaicPower/OriginData/train_{0}.csv"
index=1
duration = 1000

data  = pd.read_csv(path.format(index))

# label = data[(data["辐照度"]==-1) &((data["实际功率"]<-0.01)&(data["实际功率"]>-0.03))]["实际功率"]
# label = data[(data["辐照度"]!=-1)]["实际功率"]
# feature = data[(data["辐照度"]!=-1)]["辐照度"]
# fuzhaodu =data[(data["辐照度"]==-1)]["湿度"]

# axis = [i for i in range(len(label))]
# plt.plot(axis,label,color="blue",label= "best")
# plt.scatter(axis,label,color="blue",label= fea)
# plt.scatter(axis,fuzhaodu,color="red",label= "湿度")

# res1 = pd.read_csv(pu.predict_rootpath +"1.csv")
# res2 = pd.read_csv(pu.predict_rootpath +"2.csv")

# label1 = res1["predicition"]
# label2 = res2["predicition"]
# fea ="风向"
# label = data["实际功率"].values[200:400]
#
#
#
# axis = data["时间"].values[200:400]
label =data[["实际功率"]].values
fengxiang = data[["风向"]].apply(lambda x:math.log2(x+1),axis=1).values
axis =[i for i in range(len(label))]
plt.scatter(axis,fengxiang,color = "blue",label= "风向")
plt.scatter(axis,label,color = "red",label= "实际功率")
# plt.plot(axis,fea,color = "red",label= "fea")

# plt.plot(axis,wendu,color = "green",label= "wendu")
# plt.plot(axis,wendu_before1,color = "blue",label= "wendu_before1")
#



# plt.plot(axis,label2,color = "green",label= "second")
#
plt.legend()
plt.show()



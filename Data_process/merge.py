import  pandas as pd
import Utils.PathUtils as pu

# dir = "predict/"
dir = "model1Predict/"
path = "C:/Users/Tobin/PycharmProjects/PhotovoltaicPower/" + dir +  "{0}.csv"

test1 = pd.read_csv(path.format("1"),names=["id", "predicition"])
test2 = pd.read_csv(path.format("2"),names=["id", "predicition"])
test3 = pd.read_csv(path.format("3"),names=["id", "predicition"])
test4 = pd.read_csv(path.format("4"),names=["id", "predicition"])

# test1 = pd.read_csv(path.format("1"), names=["id", "辐照度", "predicition"])
# test2 = pd.read_csv(path.format("2"), names=["id", "辐照度", "predicition"])
# test3 = pd.read_csv(path.format("3"), names=["id", "辐照度", "predicition"])
# test4 = pd.read_csv(path.format("4"), names=["id", "辐照度", "predicition"])
#
#
# test1["predicition"]  = test1[["predicition","辐照度"]].apply(lambda x:x["predicition"] if x["辐照度"]>-1 else 0 ,axis=1 )
# test1 = test1[["id", "predicition"]]
#
#
# test2["predicition"]  = test2[["predicition","辐照度"]].apply(lambda x:x["predicition"] if x["辐照度"]>-1 else 0 ,axis=1 )
# test2= test2[["id", "predicition"]]
#
#
# test3["predicition"]  = test3[["predicition","辐照度"]].apply(lambda x:x["predicition"] if x["辐照度"]>-1 else 0 ,axis=1 )
# test3 = test3[["id", "predicition"]]
#
#
# test4["predicition"]  = test4[["predicition","辐照度"]].apply(lambda x:x["predicition"] if x["辐照度"]>-1 else 0 ,axis=1 )
# test4 = test4[["id", "predicition"]]
res = pd.concat([test1,test2,test3,test4],axis=0)
res.to_csv(pu.predict_rootpath+"res.csv",index=None)


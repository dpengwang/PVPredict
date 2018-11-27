import  pandas as pd
import Utils.PathUtils as pu
import Utils.DateUtil as du
import Utils.FeatureUtil as fu
# pd.set_option('display.max_columns', 1000)
#
# pd.set_option('display.width', 1000)
#
# pd.set_option('display.max_colwidth', 1000)

pd.set_option("display.max_columns",5000)
pd.set_option("display.max_rows",5000)
pd.set_option("display.width",1000)
pd.set_option("display.max_colwidth",100)

def get_high_corr_Feature(data):
    features = fu.base_feature
    for i in range(len(features)):
        for j in range(i+1,len(features)):
            fea1 = features[i]
            fea2 = features[j]
            data[fea1 + "+" + fea2] = data[fea1] + data[fea2]
            data[fea1 + "-" + fea2] = data[fea1] - data[fea2]
            data[fea1 + "*" + fea2] = data[fea1] * data[fea2]
            data[fea1 + "/" + fea2] = data[fea1]/data[fea2]
            data[fea2 + "/" + fea1] = data[fea2]/data[fea1]

            data[fea1 + "^2/" + fea2] =data[fea1]*data[fea1] /data[fea2]
            data[fea1 + "/" + fea2 + "^2"] = data[fea1]/(data[fea2]*data[fea2])
            data[fea2 + "^2/" + fea1] = data[fea2] * data[fea2] / data[fea1]
            data[fea2 + "/" + fea1 + "^2"] = data[fea2] / (data[fea1] * data[fea1])

    corr =data.corr()
    res = []
    for i in range(len(features)):
        for j in range(i+1,len(features)):
            fea1 = features[i]
            fea2 = features[j]
            corr1 = corr.loc["实际功率",fea1]
            corr2 = corr.loc["实际功率",fea2]
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea1 + "+" + fea2],"{0}".format(fea1 + "+" + fea2)))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea1 + "-" + fea2],"{0}".format(fea1 + "-" + fea2)))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea1 + "*" + fea2],"{0}".format(fea1 + "*" + fea2)))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea1 + "/" + fea2],"{0}".format(fea1 + "/" + fea2)))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea2 + "/" + fea1],"{0}".format(fea2 + "/" + fea1)))

            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea1 + "^2/" + fea2],"{0}".format(fea1 + "^2/" + fea2)))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea1 + "/" + fea2 + "^2"],"{0}".format(fea1 + "/" + fea2 + "^2")))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea2 + "^2/" + fea1],"{0}".format(fea2 + "^2/" + fea1)))
            res.append("{0},{1},{2},{3}".format(corr1,corr2,corr.loc["实际功率",fea2 + "/" + fea1 + "^2"],"{0}".format(fea2 + "/" + fea1 + "^2")))
    add_features = []
    for item in res:
        item = item.split(",")
        corr1 =abs(float(item[0]))
        corr2 =abs(float(item[1]))
        corr3 =abs(float(item[2]))
        # if corr3 > corr1+ corr2:
        if corr3>corr1 or corr3 > corr2:
            print(item[3])
            add_features.append(item[3])

    return add_features



def add_high_error_Feature(add_features,data):
    for feature in add_features:
        op = ""
        for item in ["+", "-", "*", "/"]:
            if item in feature:
                op = item
                break
        print(feature, op)
        fea1 = feature.split(op)[0]
        fea2 = feature.split(op)[1]

        singlefea1 = fea1 if "^" not in fea1 else fea1[:-2]
        singlefea2 = fea2 if "^" not in fea2 else fea2[:-2]
        df1 = data[singlefea1] if "^" not in fea1 else data[singlefea1]*data[singlefea1]
        df2 = data[singlefea2] if "^" not in fea2 else data[singlefea2]*data[singlefea2]
        data[feature] = {
            "+": df1+df2,
            "-": df1-df2,
            "*": df1*df2,
            "/": df1/df2
        }.get(op, "error")
    return data
data = pd.read_csv(pu.train1_path)
add_features  =get_high_corr_Feature(data[list(data.columns)])
print(add_high_error_Feature(add_features,data))




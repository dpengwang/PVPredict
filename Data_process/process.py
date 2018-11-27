import numpy as np
import pandas as pd
import Utils.PathUtils as pu
import Utils.DateUtil as du
import Utils.CommonUtil as cu
import Utils.FeatureUtil as fu
from sklearn.preprocessing import PolynomialFeatures
import  pickle
import swifter


class FeatureEngineering():

    def __init__(self, dataType,dataStation):
        self.dataType = dataType
        self.dataStation = dataStation
        self.silimarMap  = self.load_obj("similarMap_{0}".format(self.dataStation))
        self.countMap = self.load_obj("countMap_" + self.dataStation)

    def load_obj(self,name):
        with open(pu.map_rootpath + name + ".pkl","rb") as f:
            return pickle.load(f)

    def find_in_CountMap(self,key,suffix,fea_dict):
        if key in fea_dict:
            return fea_dict[key][suffix]
        else :
            devivation = float("inf")
            flag_key = ""
            for map_key in fea_dict:
                if abs(key-map_key) < devivation:
                    devivation = abs(key-map_key)
                    flag_key = map_key
            return fea_dict[flag_key][suffix]

    def find_in_SimilarMap(self,findkey):
        res = 0
        deviation = float("inf")
        for key,value in self.silimarMap.items():
            key  =list(map(float,key.split("#")))
            if self.euc_distance(findkey,key) < deviation:
                if self.euc_distance(findkey,key)==0:continue
                deviation = self.euc_distance(findkey,key)
                res = value
        return value

    def euc_distance(self,array1,array2):
        res = 0
        pair = zip(array1,array2)
        for (a,b) in pair:
            res += (a-b)**2
        return res

    def remove_dirty_data(self,origin_data):
        data = pd.DataFrame(origin_data[["时间", "实际功率"]])
        data["时间"] = data["时间"].apply(lambda x: x.split(" ")[0])
        res = data["实际功率"].groupby(data["时间"]).sum()
        res = pd.DataFrame(res).reset_index()

        y = res[["实际功率"]].iloc[:, 0].values
        x = res[["时间"]].iloc[:, 0].values

        mean = sum(list(y)) / len(y)
        high = int(mean * 1.7)
        low = int(mean * 0.3)
        badtime = []

        for i in range(len(y)):
            if int(y[i]) not in range(low, high):
                badtime.append(x[i])
        origin_data = origin_data[origin_data["时间"].apply(lambda x: x.split(" ")[0] not in badtime)]
        # origin_data = origin_data[origin_data["辐照度"]!=-1]


        if self.dataStation =="1":
            origin_data = origin_data[~((origin_data["辐照度"] == -1) & ((origin_data["实际功率"] > -0.015) | (origin_data["实际功率"] < -0.03)))]
        elif self.dataStation == "2":
            origin_data = origin_data[~((origin_data["辐照度"] == -1) & ((origin_data["实际功率"]!=0)))]
        elif self.dataStation =="3":
            origin_data = origin_data[~((origin_data["辐照度"] == -1) & ((origin_data["实际功率"] > 0)))]
        else:
            origin_data = origin_data[~((origin_data["辐照度"] == -1) & ((origin_data["实际功率"] != 0)))]


        origin_data = origin_data.drop_duplicates()
        origin_data = origin_data.reset_index(inplace=False)
        origin_data = origin_data.drop(["index"], axis=1)
        return origin_data

    def load_data(self):
        data = pd.read_csv(pu.root_data_path + "{0}_{1}.csv".format(self.dataType, self.dataStation))
        return data

#产生所有feature
    def feature_extract(self):
        print(fu.base_feature)
        data = self.load_data()
        if self.dataType == "train":
            data = self.remove_dirty_data(data)
            data  =data.drop(["实发辐照度"],axis=1)
        # data = self.shift_process(data)
        data = self.formatData(data)

        # data = self.bucketData(data)
        data = self.add_crossFeature(data)
        # data =self.add_high_corr_Feature(data)
        data = self.add_countFeature(data)
        # data = self.add_groupFeature(data)
        # data = self.add_mapFind_Feature(data)
        data = self.add_increase_Feature(data)
        # data = self.add_other_Feature(data)
        # data = self.modelMergeDrop(data)


        data = self.drop_Feature(data)
        return data


    def modelMergeDrop(self,data):
        baseFea =[ '风速', '风向', '温度', '压强', '湿度', 'month', 'day', 'hour', 'minute', 'day_of_year', 'minute_of_day']
        # baseFea = ['风速', '风向', 'month', 'day', 'hour', 'minute', 'day_of_year', 'minute_of_day']
        data =data.drop(baseFea,axis=1)
        return data

    def bucketData(self,data):

        features  = fu.base_feature[:]
        features.remove("风向")
        for fea in features:
            data[fea] =  data[fea]//0.01
        return data


    def formatData(self,data):
        # data["year"] = data["时间"].apply(lambda x: du.Date(x).get_date_year())
        data["month"]= data["时间"].apply(lambda x: du.Date(x).get_date_month())
        data["day"]  = data["时间"].apply(lambda x: du.Date(x).get_date_day())
        data["hour"] = data["时间"].apply(lambda x: du.Date(x).get_date_hour())
        data["minute"] =data["时间"].apply(lambda x: du.Date(x).get_date_minute())
        data["day_of_year"] = data["时间"].apply(lambda x: du.Date(x).get_day_of_year())
        data["minute_of_day"] = data["hour"]*4 + data["minute"]//15
        data["from1200"] = abs(data["minute_of_day"] - (12 * 4))
        data["from1230"] = abs(data["minute_of_day"] - (12 * 4 + 2))
        data["from1330"] = abs(data["minute_of_day"] - (13 * 4 + 2))
        data["from1300"] = abs(data["minute_of_day"] - 13 * 4)
        data["from1400"] = abs(data["minute_of_day"] - (14*4))
        data["风向"] = data["风向"].apply(lambda x: int(x//45))

        # data =data.drop(["风向"],axis=1)
        return data

    def add_crossFeature(self, data):
        features = list(data.columns)
        for fea in fu.drop_feature:
            if fea in features:
                features.remove(fea)
        rest_data = data.drop(features, axis=1)
        # features.remove("id")

        poly_transformer = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
        poly_data = pd.DataFrame(poly_transformer.fit_transform(data[features]), columns=poly_transformer.get_feature_names(features))
        res = pd.concat([rest_data, poly_data], join="inner",axis=1)
        return res

    def add_countFeature(self,data):
        for fea in fu.count_feature:
            fea_dict = self.countMap[fea]
            for suffix in fu.count_suffix:
                fea_name = fea + "_" + suffix
                data[fea_name] = data[[fea]].applymap(lambda x:self.find_in_CountMap(x,suffix,fea_dict))
        return data

    def add_groupFeature(self,data):
        cat = "-"
        data["ByMonth"] = data["month"].map(str)
        data["ByDay"] = data["month"].map(str) + cat + data["day"].map(str)
        data["ByDayHour"] = data["ByDay"] + cat + data["hour"].map(str)
        data["ByDayMinute"] = data["ByDayHour"] + cat + data["minute"].map(lambda x: str(x // 60))

        windows = ["ByMonth","ByDay","ByDayHour","ByDayMinute"]
        for window in windows:
            for fea in fu.base_feature:
                data[fea + "-" + window] = data[fea].groupby(data[window]).transform("mean")
        data = data.drop(windows,axis = 1)
        return data

    def drop_Feature(self,data):
        space = " "
        needDropFea = []
        timeFea =["month","day","hour","minute","minute_of_day","fromPick"]
        dataFea = list(data.columns)
        for fea in dataFea:
            count =0
            splitfea = fea.split(space)
            for item in splitfea:
                if item in timeFea:
                    count +=1
            if count>1:
                needDropFea.append(fea)
        data = data.drop(needDropFea,axis=1)
        return data

    def add_other_Feature(self,data):
        fea = fu.base_feature[:]
        for i in range(len(fea)):
            for j in range(i+1,len(fea)):
                fea1 =fea[i]
                fea2 =fea[j]
                data["{0}+{1}".format(fea1,fea2)] = data[fea1] + data[fea2]
                data["{0}-{1}".format(fea1, fea2)] = data[fea1] - data[fea2]
                # data["{0}*{1}".format(fea1, fea2)] = data[fea1] * data[fea2]
                # data["{0}/{1}".format(fea1, fea2)] = data[fea1]/data[fea2]
                # data["{0}/{1}".format(fea2, fea1)] = data[fea2]/data[fea1]


        return data

    def add_mapFind_Feature(self,data):
        data["similar实际功率"] = data[fu.base_feature].apply(lambda x:self.find_in_SimilarMap(list(x)),axis=1)
        return data

    def add_increase_Feature(self,data):
        for fea in fu.increase_feature:
            data[fea + "1_increase"] = data[fea] - data[fea].shift(1).fillna(data[fea].head())
            data[fea + "2_increase"] = data[fea] - data[fea].shift(2).fillna(data[fea].head())
            data[fea + "3_increase"] = data[fea] - data[fea].shift(3).fillna(data[fea].head())
            # data[fea + "_decrease"] = data[fea].shift(-1).fillna(data[fea].head()) - data[fea]
            data[fea + "_increaseRate"] = (data[fea] - data[fea].shift(1).fillna(data[fea].head()))/(data[fea].shift(1).fillna(data[fea].head()))
            # data[fea + "_decreaseRate"] = (data[fea] - data[fea].shift(-1).fillna(data[fea].head()))/(data[fea])

        return data

    def shift_process(self,data):
        # data["温度"] = data["温度"].shift(30).fillna(data["温度"].head()[0])
        # # data["湿度"] = data["湿度"].shift(30).fillna(data["湿度"].head()[0])
        # data["压强"] = data["压强"].shift(79).fillna(data["压强"].head()[0])
        # data["风速"] = data["风速"].shift(13).fillna(data["风速"].head()[0])
        # data["风向"] = data["风向"].shift(13).fillna(data["风速"].head()[0])
        data["fromPick"] = data["fromPick"].shift(65).fillna(data["fromPick"].head()[0])
        if self.dataType=="train":
            data =data[65:]
        return data

    def get_high_corr_Feature(self,data):
        data =self.formatData(data)
        data = self.remove_dirty_data(data)
        features = list(data.columns)
        aa =["实际功率","时间","id","实发辐照度"]
        for i in aa:
            if i in features:
                features.remove(i)

        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                fea1 = features[i]
                fea2 = features[j]
                data[fea1 + "+" + fea2] = data[fea1] + data[fea2]
                data[fea1 + "-" + fea2] = data[fea1] - data[fea2]
                data[fea1 + "*" + fea2] = data[fea1] * data[fea2]
                data[fea1 + "/" + fea2] = data[fea1] / data[fea2]
                data[fea2 + "/" + fea1] = data[fea2] / data[fea1]

                data[fea1 + "^2/" + fea2] = data[fea1] * data[fea1] / data[fea2]
                data[fea1 + "/" + fea2 + "^2"] = data[fea1] / (data[fea2] * data[fea2])
                data[fea2 + "^2/" + fea1] = data[fea2] * data[fea2] / data[fea1]
                data[fea2 + "/" + fea1 + "^2"] = data[fea2] / (data[fea1] * data[fea1])

        corr = data.corr()
        res = []
        for i in range(len(features)):
            for j in range(i + 1, len(features)):
                fea1 = features[i]
                fea2 = features[j]
                corr1 = corr.loc["实际功率", fea1]
                corr2 = corr.loc["实际功率", fea2]
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea1 + "+" + fea2],
                                                    "{0}".format(fea1 + "+" + fea2)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea1 + "-" + fea2],
                                                    "{0}".format(fea1 + "-" + fea2)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea1 + "*" + fea2],
                                                    "{0}".format(fea1 + "*" + fea2)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea1 + "/" + fea2],
                                                    "{0}".format(fea1 + "/" + fea2)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea2 + "/" + fea1],
                                                    "{0}".format(fea2 + "/" + fea1)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea1 + "^2/" + fea2],
                                                    "{0}".format(fea1 + "^2/" + fea2)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea1 + "/" + fea2 + "^2"],
                                                    "{0}".format(fea1 + "/" + fea2 + "^2")))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea2 + "^2/" + fea1],
                                                    "{0}".format(fea2 + "^2/" + fea1)))
                res.append("{0},{1},{2},{3}".format(corr1, corr2, corr.loc["实际功率", fea2 + "/" + fea1 + "^2"],
                                                    "{0}".format(fea2 + "/" + fea1 + "^2")))
        add_features = []
        for item in res:
            item = item.split(",")
            corr1 = abs(float(item[0]))
            corr2 = abs(float(item[1]))
            corr3 = abs(float(item[2]))
            # if corr3 > corr1+ corr2:
            if corr3 > corr1 or corr3 > corr2:
                add_features.append(item[3])

        return add_features

    def add_high_corr_Feature(self, data):
        add_features = self.get_high_corr_Feature(pd.read_csv("C:/Users/Tobin/PycharmProjects/PhotovoltaicPower/OriginData/train_{0}.csv".format(self.dataStation)))
        for feature in add_features:
            op = ""
            for item in ["+", "-", "*", "/"]:
                if item in feature:
                    op = item
                    break
            fea1 = feature.split(op)[0]
            fea2 = feature.split(op)[1]

            singlefea1 = fea1 if "^" not in fea1 else fea1[:-2]
            singlefea2 = fea2 if "^" not in fea2 else fea2[:-2]
            df1 = data[singlefea1] if "^" not in fea1 else data[singlefea1] * data[singlefea1]
            df2 = data[singlefea2] if "^" not in fea2 else data[singlefea2] * data[singlefea2]
            data[feature] = {
                "+": df1 + df2,
                "-": df1 - df2,
                "*": df1 * df2,
                "/": df1 / df2
            }.get(op, "error")
        return data



class saveData:
    def __init__(self,data,station,dataType):
        data.to_csv(pu.train_and_test_rootpath +"%s_%s.csv"%(dataType,station), index = False)

if __name__ == "__main__":
    fn = FeatureEngineering("train","1")
    data_with_cross_data = fn.feature_extract()

    data_with_cross_data.to_csv("C:/Users/Tobin/PycharmProjects/PhotovoltaicPower/processed_data/train1.csv",index = False)












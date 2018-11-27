import  pandas as pd
import Utils.PathUtils as pu
import Utils.FeatureUtil as fu
import pickle


def save_obj(obj,name):
    with open(pu.map_rootpath + name + ".pkl","wb") as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(pu.map_rootpath + name + ".pkl","rb") as f:
        return pickle.load(f)


def get_mean(array):
    return sum(array) /len(array)

def get_std(array):
    mean = get_mean(array)
    count = sum(list(map(lambda x:(x-mean)**2,array)))/len(array)
    return count**0.5

def get_range(array):
    return  max(array) - min(array)


def remove_exception_data(origin_data):
        data = pd.DataFrame(origin_data[["时间", "实际功率"]])
        data["时间"] = data["时间"].apply(lambda x: x.split(" ")[0])
        res = data["实际功率"].groupby(data["时间"]).sum()
        res = pd.DataFrame(res).reset_index()

        y = res[["实际功率"]].iloc[:, 0].values
        x = res[["时间"]].iloc[:, 0].values

        mean = sum(list(y)) / len(y)
        high = int(mean * 1.8)
        low = int(mean * 0.1)
        badtime = []

        for i in range(len(y)):
            if int(y[i]) not in range(low, high):
                badtime.append(x[i])
        origin_data = origin_data[origin_data["时间"].apply(lambda x: x.split(" ")[0] not in badtime)]
        origin_data = origin_data[origin_data["辐照度"]!=-1]
        # origin_data = origin_data[origin_data["实际功率"] > 0]

        origin_data = origin_data.reset_index(inplace=False)
        origin_data = origin_data.drop(["index"], axis=1)
        return origin_data

path_tp = "C:/Users/Tobin/PycharmProjects/PhotovoltaicPower/OriginData/train_{0}.csv"

def genCountMap():
    for i in range(1,5):
        station = str(i)
        path = path_tp.format(station)
        data = pd.read_csv(path)
        data =remove_exception_data(data)

        dictionary = {}
        for fea in fu.count_feature:
            grouped_data=data["实际功率"].groupby(data[fea])
            son_dict ={}
            for key,group in grouped_data:
                grandson_dict={}
                group = list(group)
                maxnum = max(group)
                minnum = min(group)
                stdnum = get_std(group)
                rangenum = get_range(group)
                meannum  = get_mean(group)
                grandson_dict["max"] = maxnum
                grandson_dict["min"] = minnum
                grandson_dict["std"] = stdnum
                grandson_dict["mean"] =meannum
                grandson_dict["range"] = rangenum
                son_dict[key] = grandson_dict

            dictionary[fea] = son_dict
        save_obj(dictionary,"countMap_"+station)

def genSimilarMap():
    for i in range(1, 5):
        station = str(i)
        path = path_tp.format(station)
        data = pd.read_csv(path)
        data = remove_exception_data(data)
        data = data.reset_index(inplace=False)
        data = data.drop(["index"], axis=1)
        dictionary = {}
        for index, line in data[["实际功率"]+fu.map_feature].iterrows():
            key = "#".join(map(lambda x: str(x), list(line)[1:]))
            # print(line)
            # print(key)
            value = str(line["实际功率"])
            if key not in dictionary:
                dictionary[key] = value
        save_obj(dictionary,"similarMap_"+station)


genCountMap()
genSimilarMap()
# if __name__ =="__main__":

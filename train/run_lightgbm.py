import pandas as pd
import numpy as np
import lightgbm as lgb
import matplotlib.pyplot as plt
import  Utils.FeatureUtil as fu
import Utils.PathUtils as pu
from sklearn.model_selection  import train_test_split
import  matplotlib
from  matplotlib.pyplot import  savefig
from scipy import  signal
params = {
            "objective": "regression",
            "metric": "rmse",
            "num_leaves": 60,
            "min_child_samples": 60,
            "learning_rate": 0.1,
            "bagging_fraction": 0.8,
            "feature_fraction": 0.8,
            "bagging_frequency": 5,
            "bagging_seed": 666,
            "verbosity": -1
            }


def remove_low_corr(data):

    # features = list(data.columns)
    # features =list(filter(lambda x:" " in x,features))
    # print(features)
    # corr = data.corr()
    # lowCorr_fea = []
    # for fea in features:
    #     fea1 = fea.split(" ")[0]
    #     fea2 = fea.split(" ")[1]
    #     corr1 = corr.loc["实际功率", fea1]
    #     corr2 = corr.loc["实际功率", fea2]
    #     corr3 = corr.loc["实际功率", fea]
    #     if corr3 < max(corr1,corr2):
    #         lowCorr_fea.append(fea)
    # return lowCorr_fea
    return data

def run(station):
    train_data_path = pu.train_and_test_rootpath + "{0}_{1}.csv".format("train",station)
    test_data_path = pu.train_and_test_rootpath + "{0}_{1}.csv".format("test",station)
    # train_and_test_rootpath  - modelMergeData_path
    # model1_feature   model2_feature
    train_data = pd.read_csv(train_data_path,index_col=False)
    test_data = pd.read_csv(test_data_path,index_col=False)

    # lowCoor_fea = remove_low_corr(train_data)
    # print(lowCoor_fea)
    # train_data = train_data.drop(lowCoor_fea,axis=1)
    # test_data  = test_data.drop(lowCoor_fea,axis=1)
    # print(train_data.shape)


    features = list(train_data.columns)

    for fea in ["实际功率","时间"]:
        if fea in list(features):
             features.remove(fea)


    # X = train_data[features]
    X = train_data[fu.model1_feature]
    Y = train_data["实际功率"]

    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.3, random_state=66)

    lgb_train = lgb.Dataset(X_train, Y_train)
    lgb_eval = lgb.Dataset(X_val, Y_val, reference=lgb_train)

    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=40000,
                    valid_sets=lgb_eval,
                    early_stopping_rounds=100,
                    verbose_eval=100
                    )

    # draw
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # matplotlib.use('qt4agg')
    # duration = 100
    # orgin = pd.DataFrame(Y_val).values[400:500]
    # predict = gbm.predict(X_val, num_iteration=gbm.best_iteration)[400:500]
    # axis = [i for i in range(len(orgin))]
    # plt.plot(axis, orgin, color="blue", label="origin")
    # plt.plot(axis, predict, color="red", label="predict")
    # plt.legend()
    # plt.show()
    # plt.close()

    #产生中间数据
    # predict_train_data = gbm.predict(X, num_iteration=gbm.best_iteration)
    # predict_train_data = pd.DataFrame(predict_train_data,columns=["pre"])
    # res_train = pd.concat([train_data,predict_train_data], axis=1)
    # predict_test_data  = gbm.predict(test_data[fu.model1_feature], num_iteration=gbm.best_iteration)
    # predict_test_data = pd.DataFrame(predict_test_data,columns=["pre"])
    # res_test = pd.concat([test_data, predict_test_data], axis=1)
    # res_train.to_csv(pu.train_and_test_rootpath + "train_{0}.csv".format(station), index=False, header=True)
    # res_test.to_csv(pu.train_and_test_rootpath + "test_{0}.csv".format(station), index=False, header=True)


    #预测
    test_id = test_data[["id"]]
    test_data = test_data.drop(["id","时间"], axis=1)
    # print(list(test_data.columns))
    predict_data = gbm.predict(test_data[fu.model1_feature], num_iteration=gbm.best_iteration)
    predict_data = pd.DataFrame(predict_data)
    res = pd.concat([test_id, predict_data], axis=1)
    res.to_csv(pu.modelPredict_path + "{}.csv".format(station), index=False, header=None)




stations = ["1", "2", "3", "4"]
# run("3")
for station in stations:
    # thread = threading.Thread(target=run,args=station)
    # thread.start()
    run(station)

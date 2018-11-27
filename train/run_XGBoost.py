# -*- coding: UTF-8 -*-
import xgboost as xgb
import pandas as pd
import matplotlib.pylab as plt
from sklearn.model_selection import train_test_split
import  Utils.PathUtils as pu
import matplotlib
import  Utils.FeatureUtil as fu

from matplotlib.pyplot import plot,savefig

def run(station):
    train_data_path = pu.proceed_data_path + "{0}_{1}.csv".format("train",station)
    test_data_path = pu.proceed_data_path + "{0}_{1}.csv".format("test",station)


    train_data = pd.read_csv(train_data_path)
    test_data = pd.read_csv(test_data_path)

    features = fu.model1_feature

    # features.remove("实际功率")
    # features.remove("实发辐照度")

    X = train_data[features]
    Y = train_data["实际功率"]


    train_X, valid_X, train_Y, valid_Y = train_test_split(X, Y, test_size=0.3, random_state=42)
    dtrain = xgb.DMatrix(train_X, train_Y)
    dvalid = xgb.DMatrix(valid_X, valid_Y)
    dtest  = xgb.DMatrix(test_data[fu.model1_feature])


    # 模型参数设置
    param = {'max_depth': 4, 'eta': 0.3, 'silent': 1, 'objective': 'reg:linear', 'reg_lambda': 1, 'reg_alpha': 0,
             'gamma':0.1 , 'subsample': 0.8, 'n_estimators': 600, 'min_child_weight':1,
            'colsample_bytree': 0.8, 'seed': 27}

    param['nthread'] = 8
    param['eval_metric'] = 'rmse'

    evallist = [(dvalid, 'eval')]
    num_round = 20000
    bst = xgb.train(param, dtrain, num_round, evallist, early_stopping_rounds=30)

   #查看验证集

    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # matplotlib.use('qt4agg')
    # duration =100
    # orgin = pd.DataFrame(valid_Y).values[600:700]
    # valid_X  =xgb.DMatrix(valid_X)
    # predict = bst.predict(valid_X, ntree_limit=num_round)[600:700]
    # axis = [i for i in range(len(orgin))]
    # print(type(predict))
    # plt.plot(axis,orgin,color="blue",label="origin")
    # plt.plot(axis, predict, color="red", label="predict")
    # # savefig(pu.predict_rootpath+"{0}.jpg".format(station))
    # plt.legend()
    # plt.show()
    #


    # 生成test
    pre_y = bst.predict(dtest, ntree_limit=num_round)
    pre_y_clo = pd.DataFrame(pre_y,columns=["predicition"])

    pre_y_clo = pd.concat([test_data["id"],pre_y_clo],axis=1)
    output_base_path = pu.predict_rootpath+station + ".csv"
    pre_y_clo.to_csv(output_base_path, header=False ,index=None)
    print("result saving at:"+output_base_path)

    # plot = xgb.plot_importance(bst, max_num_features=20)
    # plot

    feat_imp = pd.Series(bst.get_fscore()).sort_values(ascending=False)
    res_str = feat_imp.to_string()
    file_storefeature = pu.feature_importance_rootpath + station + ".txt"
    with open(file_storefeature,"w") as f:
        f.write(res_str)


stations = ["1","2","3","4"]

for station in stations:
    # thread = threading.Thread(target=run,args=station)
    # thread.start()
    run(station)
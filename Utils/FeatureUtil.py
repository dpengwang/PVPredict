base_feature = ["辐照度", "风速", "风向", "温度", "压强", "湿度"]

drop_feature = ["id", "实发辐照度", "实际功率", "时间"]

cross_feature = ["压强", "湿度", "辐照度", "温度", "风速", "风向"]

count_suffix = ["std", "range", "mean", "max", "min"]

count_feature = ["辐照度"]

nouse_feature = ["时间"]# ["风速","风向"]

map_feature = ["辐照度"]

increase_feature =["辐照度",  "温度", "压强", "湿度","风速","风向"]

corr_feature =['辐照度', '风速', '风向', '温度', '压强', '湿度', 'month', 'day', 'hour', 'minute', 'day_of_year', 'minute_of_day', 'fromPick']


increase = 1
model1_feature = ["辐照度",
                  "from1230",
                  "辐照度1_increase",
                  # "辐照度_increaseRate",
                  "温度1_increase",
                  "压强1_increase",
                  "湿度1_increase",
                  "风速1_increase",
                  "风向1_increase"
                  ]#["辐照度","fromPick","辐照度_{0}increase".format(increase),"温度_{0}increase".format(increase),"压强_{0}increase".format(increase),"湿度_{0}increase".format(increase),"风速_{0}increase".format(increase)]

# model2_feature = [ '辐照度', '风速', '温度', '压强', '湿度', 'month', 'day', 'hour', 'minute', 'day_of_year', 'minute_of_day', 'fromPick', '辐照度 风速', '辐照度 温度', '辐照度 压强', '辐照度 湿度', '辐照度 month', '辐照度 day', '辐照度 hour', '辐照度 minute', '辐照度 day_of_year', '辐照度 minute_of_day', '辐照度 fromPick', '风速 温度', '风速 压强', '风速 湿度', '风速 month', '风速 day', '风速 hour', '风速 minute', '风速 day_of_year', '风速 minute_of_day', '风速 fromPick', '温度 压强', '温度 湿度', '温度 month', '温度 day', '温度 hour', '温度 minute', '温度 day_of_year', '温度 minute_of_day', '温度 fromPick', '压强 湿度', '压强 month', '压强 day', '压强 hour', '压强 minute', '压强 day_of_year', '压强 minute_of_day', '压强 fromPick', '湿度 month', '湿度 day', '湿度 hour', '湿度 minute', '湿度 day_of_year', '湿度 minute_of_day', '湿度 fromPick', 'month day_of_year', 'day day_of_year', 'hour day_of_year', 'minute day_of_year', 'day_of_year minute_of_day', 'day_of_year fromPick', '辐照度_std', '辐照度_range', '辐照度_mean', '辐照度_max', '辐照度_min',"pre"]


model2_feature = [ "辐照度","辐照度1_increase","pre"]
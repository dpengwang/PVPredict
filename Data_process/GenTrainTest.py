import Data_process.process as prc

dataTypes = ["train","test"]
dataStations = ["1","2","3","4"]
# dataTypes = ["train"]
# dataStations = ["1"]
import threading
parameters = [(datatype,station) for datatype in dataTypes for station in dataStations]
print(parameters)

def run(datatype,station) :
        fn = prc.FeatureEngineering(datatype,station)
        data = fn.feature_extract()
        print("fish engineering in {0}_{1}".format(datatype,station))
        prc.saveData(data, station, datatype)
        print("fish saving in {0}_{1}".format(datatype,station))
        print(data.shape)
        print(list(data.columns))
for parameter in parameters:
    thread = threading.Thread(target=run,args=parameter)
    thread.start()
    thread.join()

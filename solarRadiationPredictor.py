import pandas as pd
import time
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import sklearn.metrics as met
import matplotlib.pyplot as plt
import datetime


def create_predictor(x_pre, y, lag, test_size):
	shifted = pd.concat([y, y.shift(-lag), y.shift(-2*lag), y.shift(-3*lag)], axis=1).dropna()
	shifted.columns = ["solarRadiation", "solarRadiation-"+str(lag), "solarRadiation-"+str(2*lag), "solarRadiation-"+str(3*lag)]

	y_lag_transposed = shifted.T[1:]
	y_lag=DataFrame(y_lag_transposed.T)
	y_transposed = shifted["solarRadiation"]
	x = pd.concat([x_pre, y_lag], axis = 1).dropna()
	x_train, x_test, y_train, y_test = train_test_split(x, y_transposed, test_size = test_size)
	lr = LinearRegression()
	lr.fit(x_train, y_train)
	return lr, x_train, x_test, y_train, y_test

def predictor_stats(x_pre, y, lag, test_size):
	print("Lag is ", lag)
	lr, x_train, x_test, y_train, y_test = create_predictor(x_pre, y, lag, test_size)
	print("Test set:")
	print(lr.score(x_test, y_test))
	print("Training set:")
	print(lr.score(x_train, y_train))
	print()

def date_to_float(x):
	return (x.hour*100 + x.minute-1200)/1200

def date_to_float_array(d):
	f = [date_to_float(x) for x in d]
	return f

def plot_predictor(x_pre, y, lag, test_size):
	predictor, x_train, x_test, y_train, y_test = create_predictor(x_pre, y, lag, test_size)
	y_predicted = predictor.predict(x_test)
	print(y_predicted)
	time_test = x_test["time"]
	zipped = zip(time_test, y_test, y_predicted)
	x_axis, y_test_sorted, y_pred_sorted = zip(*sorted(zipped))
	x_axis = [datetime.datetime.fromtimestamp(x) for x in x_axis]
	plt.plot(x_axis, y_test_sorted, 'b-',x_axis, y_pred_sorted, 'r-')
	plt.show()

def read_spaceapps_data(filename):
	df = pd.read_csv(filename, parse_dates = ['localTime'])
	print(df.head())
	df["localTime"] = date_to_float_array(df["localTime"])
	
	features = df.columns[:9].tolist()
	features.remove("date")
	#features.remove("localTime")
	features.remove("row ID")
	features.remove("windDirection")
	
	features = ["time", "localTime"]
	
	y = DataFrame(df["solarRadiation"])
	
	x_pre = df[features]
	return x_pre, y

x_pre, y = read_spaceapps_data("SpaceAppsData.csv")

for i in range(10, 30):
	predictor_stats(x_pre, y, i, 0.5)

plot_predictor(x_pre, y, 15, 0.5)
predictor, x_train, x_test, y_train, y_test = create_predictor(x_pre, y, 15, 0.5)
curr_time = 1475315718

data_set = DataFrame([curr_time, date_to_float(datetime.datetime.fromtimestamp(curr_time)),1.27, 1.25, 1.25]).T
data_point = data_set
predictions = []
time_list = []

for x in range(1, 288):
	fdp_prediction = predictor.predict(data_point)
	data_point_time = x*300+curr_time
	date_obj = datetime.datetime.fromtimestamp(data_point_time)
	data_point = DataFrame([data_point_time, date_to_float(datetime.datetime.fromtimestamp(data_point_time)),fdp_prediction, data_point[1], data_point[2]]).T
	data_set.append(data_point)
	predictions.append(fdp_prediction.tolist())
	time_list.append(date_obj)

plt.plot(time_list, predictions)
plt.show()
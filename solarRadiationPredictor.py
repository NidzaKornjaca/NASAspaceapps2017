import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import sklearn.metrics as met
import matplotlib.pyplot as plt


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


df = pd.read_csv("SpaceAppsData.csv")

features = df.columns[:9].tolist()
features.remove("date")
features.remove("localTime")
features.remove("row ID")
features.remove("windDirection")

#features = ["time"]

y = DataFrame(df["solarRadiation"])

x_pre = df[features]

for i in range(10, 30):
	predictor_stats(x_pre, y, i, 0.5)

predictor, x_train, x_test, y_train, y_test = create_predictor(x_pre, y, 30, 0.5)
y_predicted = predictor.predict(x_test)
print(y_predicted)
time_test = x_test["time"]
zipped = zip(time_test, y_test, y_predicted)
x_axis, y_test_sorted, y_pred_sorted = zip(*sorted(zipped))
plt.plot(x_axis, y_test_sorted, 'b-',x_axis, y_pred_sorted, 'r-')
plt.show()
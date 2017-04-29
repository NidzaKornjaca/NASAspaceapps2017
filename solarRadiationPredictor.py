import pandas as pd
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import sklearn.metrics as met

def class_infor(clf, y_test, y_pred):
	print(clf)
	

df = pd.read_csv("SpaceAppsData.csv")

features = df.columns[:9].tolist()
features.remove("date")
features.remove("localTime")
features.remove("row ID")
features.remove("time")
features.remove("windDirection")


y = DataFrame(df["solarRadiation"])

x_pre = df[features]

shifted = pd.concat([y, y.shift(-5), y.shift(-10), y.shift(-15)], axis=1).dropna()
shifted.columns = ["solarRadiation", "solarRadiation-1", "solarRadiation-2", "solarRadiation-3"]

x_pre = df[features]
y_lag_transposed = shifted.T[1:]
y_lag=DataFrame(y_lag_transposed.T)
y_transposed = shifted["solarRadiation"]


x = pd.concat([x_pre, y_lag], axis = 1).dropna()

x_train, x_test, y_train, y_test = train_test_split(x, y_transposed, test_size = 0.5)

lr = LinearRegression()
lr.fit(x_train, y_train)
print(lr.score(x_test, y_test))
print(lr.score(x_train, y_train))

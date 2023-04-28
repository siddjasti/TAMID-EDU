import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#Loading data, making it into a readable format
url = "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data-original"
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'Model Year', 'Origin', 'Car Name']
dataset = pd.read_csv(url, names=column_names, delim_whitespace=True, na_values="?")

#Removes extra spaces in the data and makes floats into ints for easier training
dataset = dataset.dropna()
dataset['Origin'] = dataset['Origin'].astype(int)

#Define x and y for training
X_drop = dataset.drop('MPG', axis=1)
X = X_drop.drop('Car Name', axis=1)
y = dataset['MPG']

#Splits the databasse into training and testing (20% for testing and 80% for training)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Trains a linear regression model based on 80% training data
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

#Predicting y values baased on 80% training data
y_pred = lr_model.predict(X_test)

#Printing the R^2 of the model to show accuracy
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error For Linear Regression:", mse)

#Trains a linear regression model based on 80% training data
lr_model = RandomForestRegressor()
lr_model.fit(X_train, y_train)

#Predicting y values baased on 80% training data
y_pred = lr_model.predict(X_test)

#Printing the R^2 of the model to show accuracy
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error For RandomForrest Regression:", mse)
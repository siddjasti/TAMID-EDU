import pandas as pd
import datetime
from pandas_datareader import wb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy
import tkinter as tk
from tkinter import ttk

#Commannd to get data set with countries from start to end data
def fetch_data(indicators, country_codes, start_date, end_date):
    data = wb.download(indicator=indicators, country=country_codes, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    return data

#Variables
indicators = ["NY.GDP.MKTP.KD", "SP.POP.TOTL", "SL.UEM.TOTL.ZS"] #GDP, Population, Unemployment
country_codes = ["AR", "BD", "BE", "CA", "CL", "CO", "DK", "EG", "FI", "GR", "HK", "ID", "IR", "IE", "IL", "IT", "KE", "KR", "MY", "MX", "NL", "NZ", "NG", "NO", "PK", "PE", "PH", "PL", "PT", "RU", "SA", "SG", "ZA", "ES", "SE", "CH", "TW", "TH", "TR", "AE", "UA", "VN"]
start_date = '2000'
end_date = '2021'

#Getting data using fetch command and alinging it with the collumns: Country, Year, GDP, Population, and Uncemployment
data = fetch_data(indicators, country_codes, start_date, end_date)
data.columns = ['Country', 'Year', 'GDP', 'Population', 'Unemployment']
data.dropna(inplace=True)

#Makes X and Y variables according to the data, then trains the x and y train variables according to LinearRegression
X = data[['GDP', 'Population']]
y = data['Unemployment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

#Uses the 20% testing size to see if our regression is accurate
y_pred = lr_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
#print(f'R^2 Score: {r2:.2f}')

country_name_to_code = {
    'Argentina': 'AR',
    'Bangladesh': 'BD',
    'Belgium': 'BE',
    'Canada': 'CA',
    'Chile': 'CL',
    'Colombia': 'CO',
    'Denmark': 'DK',
    'Egypt': 'EG',
    'Finland': 'FI',
    'France': 'FR',
    'Germany': 'DE',
    'Greece': 'GR',
    'Hong Kong': 'HK',
    'India': 'IN',
    'Indonesia': 'ID',
    'Iran': 'IR',
    'Ireland': 'IE',
    'Israel': 'IL',
    'Italy': 'IT',
    'Japan': 'JP',
    'Kenya': 'KE',
    'South Korea': 'KR',
    'Malaysia': 'MY',
    'Mexico': 'MX',
    'Netherlands': 'NL',
    'New Zealand': 'NZ',
    'Nigeria': 'NG',
    'Norway': 'NO',
    'Pakistan': 'PK',
    'Peru': 'PE',
    'Philippines': 'PH',
    'Poland': 'PL',
    'Portugal': 'PT',
    'Russia': 'RU',
    'Saudi Arabia': 'SA',
    'Singapore': 'SG',
    'South Africa': 'ZA',
    'Spain': 'ES',
    'Sweden': 'SE',
    'Switzerland': 'CH',
    'Taiwan': 'TW',
    'Thailand': 'TH',
    'Turkey': 'TR',
    'United Arab Emirates': 'AE',
    'Ukraine': 'UA',
    'United Kingdom': 'GB',
    'United States': 'US',
    'Vietnam': 'VN'
}

#Get country information based on an inputted code
def get_country_data(country_code, start_date, end_date):
    indicators = ["NY.GDP.MKTP.KD", "SP.POP.TOTL"]
    country_data = fetch_data(indicators, [country_code], start_date, end_date)
    country_data.columns = ['Country', 'Year', 'GDP', 'Population']
    return country_data

#Predicts the unemployment of another country given the regresssion we made
def predict_unemployment(country_name, model):
    country_code = country_name_to_code.get(country_name)

    country_data = get_country_data(country_code, 2000, 2021)
    country_data.dropna(inplace=True)
    
    if country_data.empty:
        print(f"No data available for country code: {country_code}")
        return None
    else:
        X_input = country_data[['GDP', 'Population']]
        unemployment_pred = model.predict(X_input)
        return numpy.mean(unemployment_pred)

#When we press the predict button, it was run the predict unemploymet command
def on_submit():
    country_name = entry_country_code.get()
    predicted_unemployment = predict_unemployment(country_name, lr_model)
    label_result.config(text=f"Predicted unemployment rate: {predicted_unemployment}%")

#All code for buttons and text fields
root = tk.Tk()
root.title("Unemployment Predictor")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_country_code = ttk.Label(frame, text="Enter country code:")
label_country_code.grid(column=0, row=0, sticky=tk.W)

entry_country_code = ttk.Entry(frame, width=10)
entry_country_code.grid(column=1, row=0)

button_submit = ttk.Button(frame, text="Predict Unemployment", command=on_submit)
button_submit.grid(column=2, row=0, padx=(10, 0))

label_possible_codes = ttk.Label(frame, text=f"R-Squared of Regresssion: {r2}")
label_possible_codes.grid(column=0, row=1, columnspan=3, pady=(5, 0), sticky=tk.W)

label_result = ttk.Label(frame, text="")
label_result.grid(column=0, row=2, columnspan=3, pady=(10, 0), sticky=tk.W)

root.mainloop()

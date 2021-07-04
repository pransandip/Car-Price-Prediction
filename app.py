# Importing necessary pakages
from flask import Flask, render_template, redirect, url_for, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))


@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/result/<float:price>")
def result(price):
    # Price checker result html page
    if price < 0:
        return render_template('result.html', prediction_text="Sorry you cannot sell this car")
    else:
        return render_template('result.html', prediction_text="You Can Sell The Car at", price=price)


@app.route("/submit", methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    output = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        elif(Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Year = 2020-Year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual == 'Individual'):
            Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0

        Transmission_Mannual = request.form['Transmission_Mannual']
        if(Transmission_Mannual == 'Mannual'):
            Transmission_Mannual = 1
        else:
            Transmission_Mannual = 0

        prediction = model.predict([[Present_Price, Kms_Driven, Owner, Year, Fuel_Type_Diesel,
                                   Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
        output = round(prediction[0], 2)

    return redirect(url_for('result', price=output))


if __name__ == "__main__":
    app.run(debug=True)

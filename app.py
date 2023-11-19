from flask import Flask, render_template, request
import os
import pathlib
import numpy as np
import pandas as pd

from src.ChurnPrediction import logger
from src.ChurnPrediction.pipeline.prediction import PredictionPipeline, CustomData

# initializing flask app
app = Flask(__name__)

@app.route('/', methods = ['GET']) # the route to display home page
def homepage():
    logger.info('Home page')
    return render_template('index.html')

@app.route('/train', methods = ['GET'])
def training():
    logger.info('Training initiated through web page')
    os.system("python main.py")
    logger.info('Training completed through web page')
    return "Training completed successfully."

@app.route('/predict', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            logger.info('Getting inputs from web page form.')

            form_data = list(request.form.values()) 
            print(form_data) 

            data = { 
                    "gender" : form_data[0],
                    "Dependents" : form_data[1],
                    "SeniorCitizen" : 1 if form_data[2] == 'Yes' else 0,
                    "Partner" : form_data[3],
                    "PhoneService" : form_data[4],
                    "MultipleLines" : form_data[5],
                    "InternetService" : form_data[6],
                    "OnlineSecurity" : form_data[7],
                    "OnlineBackup" : form_data[8],
                    "DeviceProtection" : form_data[9],
                    "TechSupport" : form_data[10], 
                    "StreamingTV" : form_data[11], 
                    "StreamingMovies" : form_data[12], 
                    "Contract" : form_data[13], 
                    "PaperlessBilling" : form_data[14], 
                    "PaymentMethod" : form_data[15],
                    "MonthlyCharges" : float(form_data[16]),
                    "tenure" : float(form_data[17]),
                    "TotalCharges" : float(form_data[18])
                    }
            
            logger.info(data)

            object_for_data_frame = CustomData(dict(data))
            data_df = object_for_data_frame.get_data_as_dataframe()
            logger.info("data transformed into dataframe")
            
            logger.info('Starting prediciton')
            prediction_object = PredictionPipeline()
            final_prediction = prediction_object.predict(data_df)
            logger.info(f'final prediction done:  {final_prediction}')

            return render_template('results.html', prediction = str('Churn' if final_prediction == 1 else 'No Churn'))

        except Exception as e:
            raise e

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug=True)
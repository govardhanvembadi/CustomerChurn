#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import joblib
from pathlib import Path
import mlflow
import os
from streamlit import runtime
from ChurnPrediction.utils.common import create_directory

def main(model, preprocessor_object):
    #Setting Application title
    st.title('Telecom Customer Churn Prediction Application')

      #Setting Application description
    st.markdown("""
     :dart:  This Streamlit app is made to predict customer churn in a ficitional telecommunication use case.
    The application is functional for both online prediction and batch data prediction. \n
    """)
    st.markdown("<h3></h3>", unsafe_allow_html=True)

    #Setting Application sidebar default
    image = Image.open('App.jpg')
    add_selectbox = st.sidebar.selectbox("How would you like to predict?", ("Online", "Batch"))
    st.sidebar.markdown('<b>This app is created to predict Customer Churn</b>', unsafe_allow_html=True)
    st.sidebar.image(image)

    if add_selectbox == "Online":
        st.markdown("<h3>Input data below</h3>", unsafe_allow_html=True)
        #Based on our optimal features selection
        st.subheader("Demographic data")
        seniorcitizen = st.selectbox('Senior Citizen:', ('Yes', 'No'))
        dependents = st.selectbox('Dependent:', ('Yes', 'No'))
        gender = st.selectbox('gender:', ('Male', 'Female'))
        partner = st.selectbox('Partner:', ('Yes', 'No'))


        st.subheader("Payment data")
        tenure = st.slider('Number of months the customer has stayed with the company', min_value=0, max_value=72, value=0)
        contract = st.selectbox('Contract', ('Month-to-month', 'One year', 'Two year'))
        paperlessbilling = st.selectbox('Paperless Billing', ('Yes', 'No'))
        PaymentMethod = st.selectbox('PaymentMethod',('Electronic check', 'Mailed check', 'Bank transfer (automatic)','Credit card (automatic)'))
        monthlycharges = st.number_input('The amount charged to the customer monthly', min_value=0, max_value=150, value=0)
        totalcharges = st.number_input('The total amount charged to the customer',min_value=0, max_value=10000, value=0)

        st.subheader("Services signed up for")
        mutliplelines = st.selectbox("Does the customer have multiple lines",('Yes','No','No phone service'))
        phoneservice = st.selectbox('Phone Service:', ('Yes', 'No'))
        deviceprotection = st.selectbox('DeviceProtection:', ('Yes', 'No'))
        internetservice = st.selectbox("Does the customer have internet service", ('DSL', 'Fiber optic', 'No'))
        onlinesecurity = st.selectbox("Does the customer have online security",('Yes','No','No internet service'))
        onlinebackup = st.selectbox("Does the customer have online backup",('Yes','No','No internet service'))
        techsupport = st.selectbox("Does the customer have technology support", ('Yes','No','No internet service'))
        streamingtv = st.selectbox("Does the customer stream TV", ('Yes','No','No internet service'))
        streamingmovies = st.selectbox("Does the customer stream movies", ('Yes','No','No internet service'))

        data = {
                'SeniorCitizen':  1 if seniorcitizen == 'Yes' else 0,
                'gender' : gender,
                'Partner' : partner,
                'DeviceProtection' : deviceprotection,
                'Dependents': dependents,
                'tenure': float(tenure),
                'PhoneService': phoneservice,
                'MultipleLines': mutliplelines,
                'InternetService': internetservice,
                'OnlineSecurity': onlinesecurity,
                'OnlineBackup': onlinebackup,
                'TechSupport': techsupport,
                'StreamingTV': streamingtv,
                'StreamingMovies': streamingmovies,
                'Contract': contract,
                'PaperlessBilling': paperlessbilling,
                'PaymentMethod':PaymentMethod, 
                'MonthlyCharges': float(monthlycharges), 
                'TotalCharges': float(totalcharges)
                }
        
        features_df = pd.DataFrame.from_dict([data])
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.write('Overview of input is shown below')
        st.markdown("<h3></h3>", unsafe_allow_html=True)
        st.dataframe(features_df)


        #Preprocess inputs
        preprocess_df = preprocessor_object.transform(features_df)
        print(preprocess_df)

        prediction = model.predict(preprocess_df)

        if st.button('Predict'):
            if prediction == 1:
                st.markdown("<h2 style = 'color:red;'>Yes, the customer will not Retain the servies.</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style = 'color:green;'>No, the customer will Retain the services.</h2>", unsafe_allow_html=True)
        

    else:
        st.subheader("Dataset upload")
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            #Get overview of data
            st.write(data.head())
            st.markdown("<h3></h3>", unsafe_allow_html=True)
            #Preprocess inputs
            preprocess_df = preprocessor_object.transform(data)
            if st.button('Predict'):
                #Get batch prediction
                prediction = model.predict(preprocess_df)
                prediction_df = pd.concat([data['customerID'],pd.DataFrame(prediction, columns=["Predictions"])], axis = 1)
                prediction_df = prediction_df.replace({1:'Yes, the customer will not Retain services.', 
                                                    0:'No, the customer will Retain services.'})

                st.markdown("<h3></h3>", unsafe_allow_html=True)
                st.subheader('Prediction')
                st.write(prediction_df)

            
if __name__ == '__main__':

    if runtime.exists():
        # And the root-level secrets are also accessible as environment variables:
        try:
            os.environ["MLFLOW_TRACKING_URI"] = st.secrets["MLFLOW_TRACKING_URI"]
            os.environ["MLFLOW_TRACKING_PASSWORD"] = st.secrets["MLFLOW_TRACKING_PASSWORD"]
            os.environ["MLFLOW_TRACKING_PASSWORD"] = st.secrets["MLFLOW_TRACKING_PASSWORD"]
        except Exception as e:
            raise e
        
        # Load model as a PyFuncModel.
        logged_model = f'runs:/{st.secrets["run_id"]}/model'
        model = mlflow.pyfunc.load_model(logged_model)

        # load preprocessor object from mlflow artifacts belonging to given 'run_id'
        create_directory([Path("local_artifacts")])
        path = mlflow.artifacts.download_artifacts(run_id = st.secrets['run_id'],artifact_path= "model/preprocessor.joblib", dst_path="local_artifacts") 
        preprocessor_object = joblib.load(path)

    else:

        model = joblib.load(Path('artifacts/model/model.joblib'))
        # load the preprocessing object
        preprocessor_object = joblib.load(Path('artifacts/model/preprocessor.joblib'))


    # call the main function
    main(model = model, preprocessor_object= preprocessor_object)

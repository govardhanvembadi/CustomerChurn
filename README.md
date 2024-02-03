# Telecom Customer Churn Prediction

![App Screenshot](app.jpg)

## Overview
Predicting customer churn in the telecom industry means trying to find out which customers might leave for another service. To do this, we use smart computer programs called machine learning models. These models look at past customer information like who they are, how they use the service, how they pay, and how well the network works. By studying all these details, the models learn to predict if a customer is likely to leave soon.

Why is this important? Well, if we can predict who might leave, we can take steps to keep them happy. Maybe we offer them a better deal or improve our services. This project uses these predictions to come up with plans to keep customers around. It also keeps an eye on things in real-time, so if customer behavior changes, we can react quickly.

In the end, the goal is to make customers happy, use our marketing efforts wisely, and make sure fewer customers decide to switch. This helps the telecom company earn more money and stay competitive in the fast-paced telecom market.

### **Data set** : [telco-customer-churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
### **Streamlit-App** : [Telecom Customer-Churn predcition](https://appapppy-yq4zcdcq8wnggnqtk93bff.streamlit.app/)


### Data Exploration:

In the initial phase of the project, data exploration involved digging into the telecom dataset to understand its characteristics. I examined customer demographics, call records, billing information, and service usage patterns. Visualizations helped reveal insights, such as identifying trends, outliers, and potential factors influencing customer churn.

See the [research/churn_prediction.ipynb](research/churn_prediction.ipynb) file for the data exploration and preprocessing phase.

### Modelling:
For predicting telecom customer churn, I employed logistic regression, a straightforward yet effective machine learning technique. Unlike linear regression, logistic regression is perfect for predicting binary outcomes, such as whether a customer will churn or not. Got almost **80%** of accuracy for the model. The algorithm analyzes various features like contract details, network performance, and customer interactions, assigning probabilities to the likelihood of churn.

### PROJECT:
1. **DVC for Data Versioning:**
   - Utilized DVC for efficient data versioning, ensuring traceability and reproducibility in managing datasets.

2. **DVC Pipelines for ML Pipelines:**
   - Implemented DVC pipelines to define machine learning pipelines, streamlining the process of managing complex workflows and dependencies.

3. **MLflow Integration for Experiment Tracking:**
   - Integrated MLflow for comprehensive experiment tracking, capturing and monitoring metrics, parameters, and artifacts throughout the machine learning model development.

4. **Dagshub URI for Model Tracking:**
   - Utilized Dagshub for model tracking and collaboration, providing a unified URI for tracking experiments, model versions, and associated metadata.

5. **Deployment with Streamlit Cloud and Flask API:**
   - Deployed the Streamlit app in the Streamlit Cloud, integrating it with a Flask API for seamless and user-friendly access to the churn prediction model.

This approach, combining DVC for data versioning and ML pipelines, MLflow for experiment tracking, and deploying the Streamlit app using Flask API, ensures a well-structured and reproducible development environment for telecom customer churn prediction.
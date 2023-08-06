Project description
============================

Usage:
================
from predictnow.pdapi import PredictNowClient1

Setup client along with its api key
api_key = "<YOUR_API_KEY>" client = PredictNowClient1(api_key)

Train demo
=================================================

train_input_path = 'C:/Users/devstack/Documents/example_input_train.csv' train_params = { "username": "welly", "email": "welly@predictnow.ai", "label": "futreturn", "timeseries": "yes", "type": "classification", "feature_selection": "shap", "analysis": "small", "boost": "gbdt", "mode": "train", "testsize": "0.2", "weights": "no", "prob_calib": "no", "suffix": "myfirstsuffix", "eda": "no", }

response = client.train(train_input_path, train_params) print(response)

Predict demo
================================
live_input_path = 'C:/Users/devstack/Documents/example_input_live.csv' username = train_params["username"] suffix = train_params["suffix"] path = "../" + train_params["username"] predict_params = { "username": username, "model_name": "saved_model_" + suffix + ".pkl", # TODO proper model name "eda": "no", } response = client.predict(live_input_path, params=predict_params) print(response)

Save Result demo
================================

response = client.save_to_output({"username": "welly", "output": "C:/Users/devstack/Documents"}) print(response)
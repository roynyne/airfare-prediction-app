import numpy as np
import pandas as pd
from datetime import datetime
from joblib import load
import lightgbm as lgb
from constants import A_PREDICTIVE_MODEL_PATH, A_AIRPORT_MAPPINGS, A_CABIN_ENCODER

class PredictionAyush:
    def __init__(self, origin: str, destination: str, flight_date: str, flight_time: str, cabin1: str, stops: str):
        self.origin = origin
        self.destination = destination
        self.flight_date = datetime.strptime(flight_date, '%Y-%m-%d')
        self.flight_time = datetime.strptime(flight_time, "%H:%M")
        self.cabin1 = cabin1
        self.stops = stops
        self.is_nonstop = 1 if stops == "0" else 0

    def preprocess_input(self):
        # Encode categorical features
        airport_encoder = load(A_AIRPORT_MAPPINGS)
        cabin_encoder = load(A_CABIN_ENCODER)

        starting_airport_encoded = airport_encoder['startingAirport'].get(self.origin, -1)
        destination_airport_encoded = airport_encoder['destinationAirport'].get(self.destination, -1)
        
        if self.cabin1 in cabin_encoder.classes_:
            cabin_code_encoded = cabin_encoder.transform([self.cabin1])[0]
        else:
            cabin_code_encoded = -1
        
        # Extract date and time features
        flight_day = self.flight_date.day
        flight_month = self.flight_date.month
        flight_year = self.flight_date.year
        departure_hour = self.flight_time.hour
        departure_minute = self.flight_time.minute
        
        # Create feature array
        features = np.array([
            starting_airport_encoded,
            destination_airport_encoded,
            cabin_code_encoded,
            self.is_nonstop,
            flight_day,
            flight_month,
            departure_hour,
            departure_minute,
            flight_year
        ]).reshape(1, -1)

        # Check for any -1 values, indicating a missing mapping
        if -1 in features:
            return {"error": "Invalid input data for one or more categorical fields."}

        return features
    
    def load_model(self):
        try:
            return lgb.Booster(model_file=A_PREDICTIVE_MODEL_PATH)
        except Exception as e:
            return {"error": f"Model loading error: {str(e)}"}
    
    def predict_fare(self, features):
        model = self.load_model()
        if isinstance(model, dict):  # Check if model loading returned an error
            return model
        
        try:
            prediction = model.predict(features, num_iteration=model.best_iteration)[0]
            return {"Prediction 3": float(round(prediction, 2))}
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}
    
    def result(self):
        # Run preprocessing and make a prediction
        features = self.preprocess_input()
        if isinstance(features, dict):  # Check if preprocessing returned an error
            return features
        
        return self.predict_fare(features)

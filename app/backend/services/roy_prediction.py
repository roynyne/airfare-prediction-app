import pandas as pd
from joblib import load
from datetime import datetime
from constants import R_PREDICTIVE_MODEL_PATH, R_DEPARTURE_TIME_ENCODER, R_CABIN_TYPE_ENCODER, R_DEPARTURE_DATE_ENCODER, R_DESTINATION_ENCODER, R_ORIGIN_ENCODER
import logging

class PredictionRoy:
    def __init__(self, origin: str, destination: str, flight_date: str, flight_time: str, cabin1: str):
        self.origin = origin
        self.destination = destination
        self.flight_date = datetime.strptime(flight_date, '%Y-%m-%d')
        self.flight_time = datetime.strptime(flight_time, "%H:%M")
        self.cabin1 = cabin1

    def preprocess_input(self):
        encoded_origin = self.safe_label_encode(R_ORIGIN_ENCODER, self.origin)
        encoded_destination = self.safe_label_encode(R_DESTINATION_ENCODER, self.destination)
        encoded_date = self.safe_label_encode(R_DEPARTURE_DATE_ENCODER, self.flight_date)
        encoded_time = self.safe_label_encode(R_DEPARTURE_TIME_ENCODER, self.flight_time)
        encoded_cabin = self.safe_label_encode(R_CABIN_TYPE_ENCODER, self.cabin1)

        features = {
            'origin_airport': [encoded_origin],
            'destination_airport': [encoded_destination],
            'departure_date': [encoded_date],
            'departure_time_HHMM': [encoded_time],
            'cabin_type': [encoded_cabin]
        }
        return pd.DataFrame(features)

    def safe_label_encode(self, encoder, value, default_value=-1):
        encoder_loaded = load(encoder)
        if value in encoder_loaded.classes_:
            return encoder_loaded.transform([value])[0]
        else:
            logging.warning(f"Unseen label '{value}' encountered. Using default value.")
            return default_value

    def load_model(self):
        try:
            return load(R_PREDICTIVE_MODEL_PATH)
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise

    def prediction_response(self, df):
        try:
            model = self.load_model()
            prediction = model.predict(df)
            result_dict = {"Prediction 2": round(prediction.tolist()[0], 2)}
            return result_dict
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise

    def result(self):
        try:
            transformed_df = self.preprocess_input()
            return self.prediction_response(transformed_df)
        except Exception as e:
            logging.error(f"Error in the prediction pipeline: {e}")
            raise
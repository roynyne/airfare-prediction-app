import pandas as pd
import requests
from datetime import datetime
import logging

class PredictionResponse:
    def __init__(self, origin: str, destination: str, date: datetime, time: datetime, 
                 current_dt: datetime, num_stops: int, cabin_type_stop1: str, 
                 cabin_type_stop2: str, cabin_type_stop3: str, cabin_type_stop4: str):
        self.origin = origin
        self.destination = destination
        self.date = date.strftime('%Y-%m-%d')  # Format date as 'YYYY-MM-DD'
        self.time = time.strftime('%H:%M')
        self.current_dt = current_dt.strftime('%Y-%m-%d')
        self.num_stops = num_stops
        self.cabin_type_stop1 = cabin_type_stop1
        self.cabin_type_stop2 = cabin_type_stop2
        self.cabin_type_stop3 = cabin_type_stop3
        self.cabin_type_stop4 = cabin_type_stop4
    
    def url_param_dict(self):
        api_request = {
            'url': 'https://airfare-backend.onrender.com/airfare/predict',
            'params': {
                "origin": self.origin, 
                "destination": self.destination, 
                "search_date": self.current_dt, 
                "flight_date": self.date,
                "flight_time": self.time, 
                "stops": self.num_stops, 
                "cabin1": self.cabin_type_stop1, 
                "cabin2": self.cabin_type_stop2,
                "cabin3": self.cabin_type_stop3, 
                "cabin4": self.cabin_type_stop4
            }
        }
        return api_request
    
    # def get_response(self):
    #     api_request = self.url_param_dict()
    #     predictions = []
        
    #     try:
    #         response = requests.get(api_request['url'], params=api_request['params'], timeout=320)
    #         response.raise_for_status()
    #         response_json = response.json()

    #         # Check if the response is a list
    #         if isinstance(response_json, list):
    #             for item in response_json:
    #                 if isinstance(item, dict):
    #                     for key, value in item.items():
    #                         if 'Prediction' in key:
    #                             predictions.append((key, value))
    #         else:
    #             print(f"Unexpected response format from {api_request['url']}.")

    #     except requests.exceptions.RequestException as e:
    #         print(f"Error fetching data from {api_request['url']}: {e}")
        
    #     return predictions
    
    def get_response(self):
        api_request = self.url_param_dict()
        predictions = []
        
        response = requests.get(api_request['url'], params=api_request['params'], timeout=320)
        response.raise_for_status()
        response_json = response.json()

        # Check if the response is a list
        if response.status_code == 200:
            for item in response_json:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if 'Prediction' in key:
                            predictions.append((key, value))
        else:
            print(f"Unexpected response format from {api_request['url']}.")
        
        return predictions

    def convert_response(self, predictions):
        if predictions:
            df = pd.DataFrame(predictions, columns=['Prediction Number', 'Predicted Airfare'])
            avg_airfare = df['Predicted Airfare'].mean()
            return df, avg_airfare
        else:
            print("No valid predictions were found.")
            return pd.DataFrame(columns=['Prediction Number', 'Prediction']), None

    def final_result(self):
        predictions = self.get_response()
        result_df, avg_airfare = self.convert_response(predictions)

        if predictions:
            return result_df, avg_airfare
        else:
            print("No valid predictions were received. The prediction service has been suspended due to inactivity, please try again later.")
            return None, None  # Return None for both if no valid predictions

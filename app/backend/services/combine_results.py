import pandas as pd
from joblib import load
from datetime import datetime
from starlette.responses import JSONResponse
from services.sidhant_prediction import PredictionSidhant
from services.roy_prediction import PredictionRoy
from services.ayush_prediction import PredictionAyush
from services.thuso_prediction import PredictionThuso
import logging

class CombinePredictions:
    def __init__(self, origin: str, destination: str, search_date: str, flight_date: str, flight_time: str, stops: str, cabin1: str, cabin2: str, cabin3: str, cabin4: str):
        # Initialize
        self.origin = origin
        self.destination = destination
        self.search_date = search_date
        self.flight_date = flight_date
        self.flight_time = flight_time
        self.stops = stops
        self.cabin1 = cabin1
        self.cabin2 = cabin2
        self.cabin3 = cabin3
        self.cabin4 = cabin4

    def get_prediction_1(self):
        prediction = PredictionSidhant(self.origin, self.destination, self.search_date, self.flight_date, 
                                       self.flight_time, self.stops, self.cabin1, self.cabin2, self.cabin3, 
                                       self.cabin4)
        return prediction.result()
    
    def get_prediction_2(self):
        prediction = PredictionRoy(self.origin, self.destination, self.flight_date, self.flight_time, self.cabin1)
        return prediction.result()
    
    def get_prediction_3(self):
        prediction = PredictionAyush(self.origin, self.destination, self.flight_date, self.flight_time, self.cabin1, self.stops)
        return prediction.result()

    def get_prediction_4(self):
        prediction = PredictionThuso(self.origin, self.destination, self.flight_date, self.flight_time, self.cabin1)
        return prediction.result()

    def combine_results(self):
        prediction_list = []

        prediction_list.append(self.get_prediction_1())
        prediction_list.append(self.get_prediction_2())
        prediction_list.append(self.get_prediction_3())
        prediction_list.append(self.get_prediction_4())

        return prediction_list
    
    def final_result(self):
        pred_list = self.combine_results()
        # Convert the list of dictionaries into a JSON-formatted string
        response = JSONResponse(content=pred_list, status_code=200)

        # Log the response content as a string
        logging.info(f"Response content: {response.body.decode()}")

        return response
        
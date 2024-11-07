import pandas as pd
from joblib import load
from datetime import datetime
from constants import S_PREDICTIVE_MODEL_PATH, S_SCALER_ENCODER, S_ORDINAL_ENCODER, S_EXTERNAL_CSV_PATH

class PredictionSidhant:
    def __init__(self, origin: str, destination: str, search_date: str, flight_date: str, flight_time: str, stops: str, cabin1: str, cabin2: str, cabin3: str, cabin4: str):
        # Initialize
        self.origin = origin
        self.destination = destination
        self.search_date = datetime.strptime(search_date, '%Y-%m-%d')
        self.flight_date = datetime.strptime(flight_date, '%Y-%m-%d')
        self.flight_time = datetime.strptime(flight_time, "%H:%M")
        self.stops = stops
        self.cabin1 = cabin1
        self.cabin2 = cabin2
        self.cabin3 = cabin3
        self.cabin4 = cabin4

    def input_data(self):
        # Extract components needed for prediction input.
        origin = self.origin
        destination = self.destination
        stops = int(self.stops)
        search_date = self.search_date
        flight_date = self.flight_date
        flight_time = self.flight_time
        cabin1 = self.cabin1
        cabin2 = self.cabin2
        cabin3 = self.cabin3
        cabin4 = self.cabin4

        # derive travel duration and distance
        distance, duration = self.retrieve_distance_duration(origin, destination, stops)

        # Calculate days difference
        days_diff = (flight_date - search_date).days

        # Extract flight date components.
        f_day = flight_date.day
        f_month = flight_date.month 

        # Extract flight time components.
        f_hour = flight_time.hour
        f_minute = flight_time.minute

        # Create a dictionary for DataFrame input.
        data_dict = {
            "startingAirport": origin,
            "destinationAirport": destination,
            "totalTravelDistance": float(distance),
            "travelDurationMins": float(duration),
            "cabinTypeSegmentSegment1": cabin1, 
            "cabinTypeSegmentSegment2": cabin2,
            "cabinTypeSegmentSegment3": cabin3,
            "cabinTypeSegmentSegment4": cabin4,
            "numStops": stops,
            "flightMonth": f_month,
            "flightDay": f_day,
            "flightHour": f_hour, 
            "flightMinute": f_minute,
            "days_difference": days_diff
        }

        # Return the input DataFrame.
        return pd.DataFrame(data_dict, index=[0])
    
    def retrieve_distance_duration(self, origin, destination, stops):

        df = pd.read_csv(S_EXTERNAL_CSV_PATH)

        # Filter data for the specific origin and destination pair
        pair_data = df[(df['startingAirport'] == origin) & (df['destinationAirport'] == destination)]
        
        # Select the appropriate travel distance and duration based on stops
        if stops == 0:
            # No stops case
            travel_distance = pair_data['avg_travel_distance_no_stops'].values[0]
            travel_duration = pair_data['avg_travel_duration_no_stops'].values[0]
        else:
            # With stops case
            travel_distance = pair_data['avg_travel_distance_with_stops'].values[0]
            travel_duration = pair_data['avg_travel_duration_with_stops'].values[0]
        
        return travel_distance, travel_duration

    def data_transformation(self, df):
        # Load necessary encoders and scalers for data transformation.
        ordinal_encoder = load(S_ORDINAL_ENCODER)
        scaler = load(S_SCALER_ENCODER)
        
        # Apply ordinal encoding for specified categorical columns.
        df[['startingAirport', 'destinationAirport', 'cabinTypeSegmentSegment1', 
            'cabinTypeSegmentSegment2', 'cabinTypeSegmentSegment3', 
            'cabinTypeSegmentSegment4']] =  ordinal_encoder.transform(df[['startingAirport', 'destinationAirport', 'cabinTypeSegmentSegment1', 
                                                                              'cabinTypeSegmentSegment2','cabinTypeSegmentSegment3', 
                                                                              'cabinTypeSegmentSegment4']])
        
        # Scale the data using the fistted scaler.
        scaled_data = scaler.transform(df)

        # Return the scaled DataFrame with original columns.
        return pd.DataFrame(scaled_data, columns=df.columns)

    def load_model(self):
        # Load the predictive model from the specified path.
        return load(S_PREDICTIVE_MODEL_PATH)

    def prediction_response(self, df):
        # Load model, make prediction, and prepare the response.
        model = self.load_model()
        prediction = model.predict(df)

        # Prepare the result dictionary with the rounded prediction.
        result_dict = {"Prediction 1": round(prediction.tolist()[0], 2)}

        return result_dict  # Return the prediction result as JSON.

    def result(self):
        # Execute the prediction pipeline and return the final prediction response.
        input_df = self.input_data()  # Gather input data.
        transformed_df = self.data_transformation(input_df)  # Transform the data.
        return self.prediction_response(transformed_df)  # Get prediction response.

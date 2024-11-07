import pandas as pd
from joblib import load
from datetime import datetime
from constants import T_PREDICTIVE_MODEL_PATH, T_CABIN_ENCODER, T_DESTINATION_ENCODER, T_ORIGIN_ENCODER

class PredictionThuso:
    def __init__(self, origin: str, destination: str, flight_date: str, flight_time: str, cabin1: str):
        # Initialize
        self.origin = origin
        self.destination = destination
        self.flight_date = datetime.strptime(flight_date, '%Y-%m-%d')
        self.flight_time = datetime.strptime(flight_time, "%H:%M")
        self.cabin1 = cabin1

    def combine_date_time_to_epoch(self, flight_date: datetime, flight_time: datetime) -> int:
        combined_datetime = pd.to_datetime(f"{flight_date.strftime('%Y-%m-%d')} {flight_time.strftime('%H:%M')}")
        epoch_time = int(combined_datetime.timestamp())
        return epoch_time

    def input_data(self):
        # Convert date and time to epoch seconds using the instance method.
        epoch_seconds = self.combine_date_time_to_epoch(self.flight_date, self.flight_time)

        # Create a dictionary for DataFrame input.
        data_dict = {
            "origin_airport": self.origin,
            "destination_airport": self.destination,
            "cabin_type": self.cabin1,
            'departure_time_seconds': epoch_seconds
        }

        # Return the input DataFrame.
        return pd.DataFrame([data_dict])

    def data_transformation(self, df):
        # Load necessary encoders and scalers for data transformation.
        cabin_encoder = load(T_CABIN_ENCODER)
        destination_encoder = load(T_DESTINATION_ENCODER)
        origin_encoder = load(T_ORIGIN_ENCODER)

        df["cabin_type"] = cabin_encoder.transform(df[["cabin_type"]])
        df["destination_airport"] = destination_encoder.transform(df[["destination_airport"]])
        df["origin_airport"] = origin_encoder.transform(df[["origin_airport"]])

        # Return the scaled DataFrame with original columns.
        return df

    def load_model(self):
        # Load the predictive model from the specified path.
        return load(T_PREDICTIVE_MODEL_PATH)

    def prediction_response(self, df):
        # Load model, make prediction, and prepare the response.
        model = self.load_model()
        prediction = model.predict(df)

        # Prepare the result dictionary with the rounded prediction.
        result_dict = {"Prediction 4": round(prediction[0], 2)}

        return result_dict

    def result(self):
        # Execute the prediction pipeline and return the final prediction response.
        input_df = self.input_data()  # Gather input data.
        transformed_df = self.data_transformation(input_df)  # Transform the data.
        return self.prediction_response(transformed_df)  # Get prediction response.
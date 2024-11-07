# Contains constant values such as filepaths and numerical values
S_PREDICTIVE_MODEL_PATH = "models/sidhant/xgboost5_final.joblib"
T_PREDICTIVE_MODEL_PATH = "models/thuso/ada_reg1.joblib"
R_PREDICTIVE_MODEL_PATH = "models/roy/rf_model.pkl"
A_PREDICTIVE_MODEL_PATH = "models/ayush/LightGBM_best_model.txt"


S_SCALER_ENCODER = "transformers/sidhant/scaler_final.joblib"
S_ORDINAL_ENCODER = "transformers/sidhant/ordinal_encoder_final.joblib"
S_EXTERNAL_CSV_PATH = "data/external.csv"

T_CABIN_ENCODER = "transformers/thuso/cabin_encoder.joblib"
T_DESTINATION_ENCODER = "transformers/thuso/cabin_encoder.joblib"
T_ORIGIN_ENCODER = "transformers/thuso/cabin_encoder.joblib"

R_CABIN_TYPE_ENCODER = "transformers/roy/cabin_type_label_encoder.pkl"
R_DEPARTURE_DATE_ENCODER = "transformers/roy/departure_date_label_encoder.pkl"
R_DEPARTURE_TIME_ENCODER = "transformers/roy/departure_time_HHMM_label_encoder.pkl"
R_DESTINATION_ENCODER = "transformers/roy/destination_airport_label_encoder.pkl"
R_ORIGIN_ENCODER = "transformers/roy/origin_airport_label_encoder.pkl"

A_AIRPORT_MAPPINGS = "transformers/ayush/airport_label_mappings.joblib"
A_CABIN_ENCODER = "transformers/ayush/segmentsCabinCode_encoder.joblib"
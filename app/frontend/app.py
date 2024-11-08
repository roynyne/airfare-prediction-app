import streamlit as st
import datetime
from services.predict import PredictionResponse

# Streamlit App
st.title("Airfare Prediction App ✈️")

st.header("Enter your travel details to predict airfare 💰", divider=True)


iata_codes = ["ATL", "BOS", "CLT", "DEN", "DFW", "DTW", "EWR", 
              "IAD", "JFK", "LAX", "LGA", "MIA", "OAK", "ORD", 
              "PHL", "SFO"]

origin = st.selectbox("Type/Select Origin Airport (IATA Code)", iata_codes)

destination = st.selectbox("Type/Select Destination Airport (IATA Code)", iata_codes)

# Get the current timestamp
current_datetime = datetime.datetime.now()

# Set default values for date and time inputs in Streamlit
departure_date = st.date_input("Departure Date", value=current_datetime.date())
departure_time = st.time_input("Departure Time", value=current_datetime.time())

# Radio button for number of stops
num_stops = st.radio("Select the number of stops:", options=[0, 1, 2, 3])

# Cabin type options
cabin_options = ["coach", "premium coach", "business", "first"]

cabin_type_stop2 = "No cabin"
cabin_type_stop3 = "No cabin"
cabin_type_stop4 = "No cabin"

# Based on the number of stops, display the appropriate number of cabin type dropdowns
if num_stops == 0:
    cabin_type_stop1 = st.selectbox("Select cabin type for non-stop flight:", cabin_options)
    st.write("Selected cabin type:", cabin_type_stop1)

elif num_stops == 1:
    cabin_type_stop1 = st.selectbox("Select cabin type for the first leg of the journey:", cabin_options)
    cabin_type_stop2 = st.selectbox("Select cabin type for the second leg of the journey:", cabin_options)
    st.write("Selected cabin types:", cabin_type_stop1, "for first leg and", cabin_type_stop2, "for second leg")

elif num_stops == 2:
    cabin_type_stop1 = st.selectbox("Select cabin type for the first leg of the journey:", cabin_options)
    cabin_type_stop2 = st.selectbox("Select cabin type for the second leg of the journey:", cabin_options)
    cabin_type_stop3 = st.selectbox("Select cabin type for the third leg of the journey:", cabin_options)
    st.write("Selected cabin types:", cabin_type_stop1, "for first leg,", cabin_type_stop2, "for second leg, and", cabin_type_stop3, "for third leg")

elif num_stops == 3:
    cabin_type_stop1 = st.selectbox("Select cabin type for the first leg of the journey:", cabin_options)
    cabin_type_stop2 = st.selectbox("Select cabin type for the second leg of the journey:", cabin_options)
    cabin_type_stop3 = st.selectbox("Select cabin type for the third leg of the journey:", cabin_options)
    cabin_type_stop4 = st.selectbox("Select cabin type for the fourth leg of the journey:", cabin_options)
    st.write("Selected cabin types:", cabin_type_stop1, "for first leg,", cabin_type_stop2, "for second leg,", cabin_type_stop3, "for third leg, and", cabin_type_stop4, "for fourth leg")

# Button to trigger prediction
if st.button("Predict Airfare"):
    if origin == destination:
        st.error("Error: The origin and destination cannot be the same. Please select different airports.")
    else:
        # Create an instance of the PredictionResponse class
        prediction_instance = PredictionResponse(
            origin=origin,
            destination=destination,
            date=departure_date,
            time=departure_time,
            current_dt=current_datetime,
            num_stops=num_stops,
            cabin_type_stop1=cabin_type_stop1,
            cabin_type_stop2=cabin_type_stop2,
            cabin_type_stop3=cabin_type_stop3,
            cabin_type_stop4=cabin_type_stop4
        )
        
        # Get the predictions
        predictions_df, avg_prediction_value = prediction_instance.final_result()
        
        if not predictions_df.empty:
            # Display the predictions DataFrame
            st.dataframe(predictions_df, 
                            hide_index=True,  
                            width=1000, 
                            column_config={
                            "Predicted Airfare": st.column_config.NumberColumn(format="＄ %d")
                            })

            # Display the average prediction value
            st.markdown(
                f"""
                <div style="text-align: center;">
                <span style="font-size: 24px; font-weight: bold;">Average Airfare ($)</span><br>
                <span style="font-size: 40px;">${avg_prediction_value:,.2f}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("No valid predictions were received. The prediction service has been suspended due to inactivity, please try again later.")
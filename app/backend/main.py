# Imports
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from services.combine_results import CombinePredictions
from services.brief import BriefResults
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Set allowed origins for CORS
origins = ["http://localhost:8501", "https://airfare-app.onrender.com"]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fast API endpoints
@app.get("/", response_class=PlainTextResponse)
def read_root():
    brief = BriefResults()
    return brief.response()

# Health endpoint
@app.get("/health", status_code=200)
def healthcheck():
    return 'Application is all ready to go!'

# Airfare Endpoint
@app.get("/airfare/predict/")
def prediction_response(origin: str, destination: str, search_date: str, flight_date: str, flight_time: str, stops: str, cabin1: str, cabin2: str, cabin3: str, cabin4: str):
    combined_result = CombinePredictions(origin, destination, search_date, flight_date, flight_time, stops, cabin1, cabin2, cabin3, cabin4)
    return combined_result.final_result()
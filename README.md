# Airfare Prediction Part 2: Deploying the Application(s)

![pexels-olly-3769146](https://github.com/user-attachments/assets/f64ab117-d98a-4e89-974b-d6d54c110ad1)


## 1. Deployment

### a. Model Serving

The airfare prediction system uses a FastAPI-based backend to serve four models: ‘

1. Random Forest
2. XG-Boost-1
3. LightGBM
4. XG-Boost-2

These models, represented by PredictionRoy, PredictionAyush, PredictionSidhant, and PredictionThuso, are stored in the "models/" directory. The backend handles incoming prediction requests by invoking specific preprocessing logic, such as label encoding, scaling, and transformations. PredictionSidhant applies scaling and ordinal encoding, while PredictionAyush uses LightGBM.

<img width="523" alt="Screenshot 2024-12-14 at 12 16 59 PM" src="https://github.com/user-attachments/assets/a24ddad3-4759-4ccf-b013-6f9ef4796ab4" />

The model class loads encoders from the "transformers/" directory, including cabin_type, departure_date, and airport label encoders, to ensure compatibility with training data. Custom transformers handle input variability, such as PredictionThuso converting date and time into epoch seconds and PredictionSidhant calculating travel duration and distance from a CSV file.

<img width="293" alt="Screenshot 2024-12-14 at 12 17 44 PM" src="https://github.com/user-attachments/assets/16755c7b-269b-4dd1-83f2-14671b7232d7" />

The FastAPI endpoint aggregates predictions from all models into a JSON response, allowing clients to view individual model outputs. CORS policies ensure secure cross-origin requests from specified origins, while the backend, containerized via Docker, runs in Python 3.11.4 and uses Uvicorn on port 8000 for consistent execution.

<img width="622" alt="Screenshot 2024-12-14 at 12 18 12 PM" src="https://github.com/user-attachments/assets/c1f10c21-1c38-4aca-a39e-b61d87238255" />

The challenges faced included maintaining consistency in preprocessing across models, handling unseen labels safely, and managing model-specific encoding schemes without errors. Special handling was needed for LightGBM's model in PredictionAyush to avoid compatibility issues, and logging and error handling were implemented.

Future improvements include centralising encoding and preprocessing logic, using a model registry for easier versioning, and deploying with Kubernetes for load balancing. Real-time monitoring tools like Prometheus and Grafana will enhance fault tolerance and scalability, ensuring a robust system capable of handling complex, model-specific transformations in real-time deployment.

### b. Web App

The Render-deployed airfare prediction web application offers a thorough, real-time price prediction service that uses machine learning to deliver pricing insights. The app delivers precise fare estimations by processing user-provided trip data, such as origin, destination, departure date and time, number of stops, and cabin type using:

Streamlit frontend (https://airfare-app.onrender.com/)

FastAPI backend (https://airfare-backend.onrender.com/)

The UI screenshot illustrates how user-friendly the frontend interface is, directing users through radio buttons for stops, dropdowns for airport codes, date and time pickers, and choose boxes for cabin kinds. The backend receives this data and uses four different models (Random Forest, XGBoost, and LightGBM) with unique preprocessing and encoding logic to provide reliable predictions.

<img width="333" alt="Screenshot 2024-12-14 at 12 18 41 PM" src="https://github.com/user-attachments/assets/b86bce20-f9a0-4851-a0c6-d1c290e14f4b" />

To deploy locally, users install dependencies, start FastAPI backend with Uvicorn on port 8000, and launch Streamlit frontend on port 8501. Docker configurations ensure reproducible environment and platform consistency. Encoders and transformers handle custom encoding for airport codes, cabin types, and date-time conversions.

<img width="369" alt="Screenshot 2024-12-14 at 12 19 04 PM" src="https://github.com/user-attachments/assets/5a96fefb-3800-47e2-8427-41dbb5028060" />

The application displays fare predictions for each model in a structured table. Users input travel details and click "Predict Airfare," which displays the predicted airfare for each model. Each prediction is labelled for comparison. The app calculates and displays the average fare, providing a consolidated estimate based on all model predictions. This feature helps users make informed decisions by viewing individual predictions and an overall average, smoothing out potential variances across models.

The tool is designed for travel agencies, airlines, and price-sensitive travellers, offering pricing intelligence and competitive analysis. Its configurability allows users to simulate various travel scenarios, making it valuable for business intelligence and demand forecasting.

The app could be licensed as a SaaS or API service for travel platforms, integrating fare predictions into booking flows. Future enhancements could include model retraining, seasonality adjustments, and continuous monitoring.

The current model has limitations like static data drift, lack of real-time updates, and customization constraints. Future upgrades may include dynamic retraining pipelines, predictive variables, and monitoring tools for improved reliability and operational robustness.

## 2. Conclusion

In the airline industry, predicting airfare prices has traditionally relied on historical data and market trends, often without a scientific approach to the multitude of factors influencing prices. With advancements in data analytics and machine learning, vast amounts of data can now inform pricing decisions more accurately.

This project demonstrates that machine learning can help businesses become more data-driven in their pricing strategies. Using a comprehensive dataset, the project explored algorithms to predict airfare prices based on various factors such as flight characteristics, historical pricing, and seasonal trends. It shows how machine learning can identify patterns for predictive analytics, allowing airlines to optimise their pricing strategies and resource allocation.

A key component of this project is the deployment of the predictive models as a web application. This web app provides an intuitive interface where users can input flight queries and receive real-time price predictions. The web app ensures that the model’s predictions are easily accessible to airlines, travel agencies, and travellers, enhancing their decision-making processes.

The deployment process involved containerizing the web service assets for ease of deployment and scalability. The application is hosted on a robust cloud infrastructure, ensuring high availability and performance. Continuous integration and continuous deployment (CI/CD) practices were implemented using a collaborative code repository to facilitate seamless updates and maintenance.

By integrating traditional data science practices with modern application development and deployment practices, machine learning products are becoming more accessible. This approach moves away from black-box practices to more transparent and effective machine learning products, ultimately benefiting the data science practitioners, businesses and customers.

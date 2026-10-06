KCET Rank Predictor & College Recommendation Platform 🎓

## Live Demo

[Open the KCET Rank Predictor](https://kcet-frontend.onrender.com)

This is a full-stack Machine Learning project that predicts KCET ranks and recommends engineering colleges using real historical cutoff data.
The project is built as a proper frontend–backend system using REST APIs and Docker, focusing on how ML applications are actually built and deployed in practice.

This is not a notebook demo. It’s a working ML product.

What This App Does

Students enter their KCET marks, board marks, and exam year.
The system predicts an approximate KCET rank and suggests colleges that are realistically achievable based on previous year cutoffs.

College recommendations can be filtered by branch, location, and college type to help students make better decisions.

How the System Is Built

The project is split into two independent services.

Streamlit Frontend 🖥
Pure UI layer
Handles user input and displays results
Communicates with backend using HTTP

FastAPI Backend ⚙️
Handles ML inference and business logic
Loads trained model, scaler, and cutoff dataset
Exposes REST APIs

The frontend and backend are fully decoupled and can be deployed independently.

Tech Stack

Backend
FastAPI
Pydantic
Scikit-learn
Pandas
NumPy

Frontend
Streamlit
Requests
Pandas

Infrastructure
Docker
Docker Compose
Docker Hub

Machine Learning Overview 🤖

The ML model is trained on historical KCET-related data.

Inputs
KCET marks
Board marks
Exam year

Processing
Feature normalization
Supervised regression model
Post-prediction adjustment to reflect real exam trends

Output
Predicted KCET rank

The backend performs inference only. Training is done offline.

College Recommendation Logic 🏫

Uses real historical KCET cutoff data
Matches predicted rank against cutoffs
Supports branch, location, and college type filters
Returns only realistically achievable colleges

Project Structure

Backend
FastAPI application
ML model and scaler
College cutoff dataset

Frontend
Streamlit application
Pure UI and API client

Docker
Separate Dockerfiles for frontend and backend
docker-compose.yml for local orchestration

Run Using Docker (Recommended 🚀)

No Python setup required. Only Docker.

Pull images from Docker Hub
docker pull venkat023/kcetpredictor-backend:latest
docker pull venkat023/kcetpredictor-frontend:latest

Run backend
docker run -d --name kcet-backend -p 8000:8000 venkat023/kcetpredictor-backend:latest

Backend API
http://localhost:8000/docs

Run frontend
docker run -d --name kcet-frontend -p 8501:8501 -e BACKEND_URL=http://host.docker.internal:8000
 venkat023/kcetpredictor-frontend:latest

Frontend UI
http://localhost:8501

API Endpoints 🔗

POST /predict – Predict KCET rank
GET /filters – Fetch available filters
POST /recommandation – Get eligible colleges

All APIs are stateless and JSON-based.

Why This Project Matters

Shows end-to-end ML system design
Uses real data and real constraints
Clean frontend–backend separation
Dockerized and cloud-ready
Built like a real ML product, not a demo

Possible Improvements

Prediction confidence intervals
Category-based cutoff support
User authentication
Better ML models
CI/CD pipeline

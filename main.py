from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS for all origins (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace * with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather")
def get_weather(city: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"error": "API key not found. Please set OPENWEATHER_API_KEY in .env file."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "City not found"}

    data = response.json()
    return {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"].capitalize(),
        "humidity": data["main"]["humidity"],
        "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    }

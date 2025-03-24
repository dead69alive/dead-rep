
import os
import requests
import openai
import streamlit as st
from dotenv import load_dotenv

# Load API keys
load_dotenv("OPENWEATHER_API_KEY.env")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Streamlit UI
st.title("Weather & Outfit Suggestion App")
city = st.text_input("Enter city name:", "")

if st.button("Get Weather & Outfit Suggestion"):
    if city:
        # Get weather data
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(base_url)

        if response.status_code == 200:
            data = response.json()
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]
            visibility = data.get("visibility", "N/A")

            # Display weather info
            st.subheader(f"Weather in {city}")
            st.write(f"**Condition:** {weather_desc.capitalize()}")
            st.write(f"**Temperature:** {temp}°C (Feels like {feels_like}°C)")
            st.write(f"**Humidity:** {humidity}%")
            st.write(f"**Wind Speed:** {wind_speed} m/s")
            st.write(f"**Pressure:** {pressure} hPa")
            st.write(f"**Visibility:** {visibility} meters")

            # Generate clothing suggestion with OpenAI
            prompt = (
                f"The weather in {city} is {weather_desc}, with a temperature of {temp}°C, "
                f"feels like {feels_like}°C, humidity of {humidity}%, wind speed of {wind_speed} m/s, "
                f"pressure at {pressure} hPa, and visibility of {visibility} meters. "
                "Give a sarcastic yet useful outfit suggestion."
            )

            ai_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                temperature=0.5,  # More randomness & sarcasm
                messages=[
                    {"role": "system", "content": "You are a a nice realistic AI that suggest clothing ."},
                    {"role": "user", "content": prompt}
                ]
            )

            clothing_suggestion = ai_response.choices[0].message.content

            # Display outfit suggestion
            st.subheader("Suggested Outfit")
            st.write(clothing_suggestion)
        else:
            st.error("Failed to retrieve weather data. Check city name and API key.")
    



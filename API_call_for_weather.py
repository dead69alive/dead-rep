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

            # Display weather info
            st.subheader(f"Weather in {city}")
            st.write(f"**Condition:** {weather_desc}")
            st.write(f"**Temperature:** {temp}°C (Feels like {feels_like}°C)")
            st.write(f"**Humidity:** {humidity}%")

            # Generate clothing suggestion with OpenAI
            prompt = (
                f"The weather in {city} is {weather_desc}, with a temperature of {temp}°C, "
                f"feels like {feels_like}°C, and {humidity}% humidity. "
                "What should someone wear for this weather?"
            )
            ai_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            clothing_suggestion = ai_response.choices[0].message.content

            # Display outfit suggestion
            st.subheader("Suggested Outfit")
            st.write(clothing_suggestion)
        else:
            st.error("Failed to retrieve weather data. Check city name and API key.")



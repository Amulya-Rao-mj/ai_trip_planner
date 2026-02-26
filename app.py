import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from utils import save_trip, load_trips, generate_pdf

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Trip Planner", page_icon="🌍", layout="wide")

st.title("🌍 AI Trip Planner")
st.write("Plan your personalized trip using AI!")

# Sidebar - Trip History
st.sidebar.title("📜 Trip History")
history = load_trips()

if history:
    for i, trip in enumerate(history[::-1]):
        st.sidebar.write(f"**{trip['destination']}** - {trip['duration']} days")
else:
    st.sidebar.write("No trips saved yet.")

st.markdown("---")

# User Inputs
col1, col2 = st.columns(2)

with col1:
    destination = st.text_input("📍 Destination")
    duration = st.number_input("🗓 Number of Days", min_value=1, max_value=30, value=5)

with col2:
    budget = st.selectbox("💰 Budget", ["Low", "Medium", "Luxury"])
    travel_style = st.multiselect(
        "🎒 Travel Style",
        ["Adventure", "Relaxation", "Food", "Culture", "Nightlife", "Nature"]
    )

if st.button("🚀 Generate Itinerary"):

    if destination:

        with st.spinner("Generating your travel plan... ✈️"):

            prompt = f"""
            Generate a structured {duration}-day travel itinerary.

            Destination: {destination}
            Budget: {budget}
            Travel Style: {', '.join(travel_style)}

            Format:
            1. Overview
            2. Day-wise plan (Day 1, Day 2...)
            3. Recommended areas to stay
            4. Must-visit attractions
            5. Food recommendations
            6. Estimated total budget
            7. Travel tips
            """

            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are an expert travel planner."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )

            itinerary = response.choices[0].message.content

        st.success("Trip Plan Generated Successfully! 🎉")
        st.markdown("## ✈️ Your Travel Itinerary")
        st.write(itinerary)

        # Save trip
        save_trip(destination, duration, budget, travel_style, itinerary)

        # Download PDF
        if st.button("📄 Download as PDF"):
            generate_pdf(itinerary)
            st.success("PDF downloaded successfully!")

    else:
        st.warning("Please enter a destination.")
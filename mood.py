import streamlit as st
import openai
import json
import os
from datetime import datetime

st.markdown("<h1 style='text-align: center;'>Mood Detector</h1>", unsafe_allow_html=True)

# Load API key
with open("keys.json") as f:
    keys = json.load(f)

client = openai.OpenAI(api_key=keys["api_key"])

# File for storing usage
USAGE_FILE = "usage_data.json"

# Initialize usage file if it doesn't exist
if not os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, "w") as f:
        json.dump({}, f)

# Load usage data
with open(USAGE_FILE, "r") as f:
    usage_data = json.load(f)

# Get today’s date
today = datetime.today().strftime("%Y-%m-%d")

# Initialize or reset global counter for today
if usage_data.get("date") != today:
    usage_data = {"date": today, "count": 0}

# Streamlit inputs
username = st.text_input("Enter your username:")
user_sentence = st.text_input("Enter a sentence – I'll detect the mood:")

if st.button("Check Mood"):
    if not username:
        st.warning("Please enter your username.")
    elif not user_sentence:
        st.warning("Please type something first!")
    else:
        if usage_data["count"] >= 10:
            st.error("❌ Max mood checks reached for today.")
        else:
            # Create prompt
            prompt = f"""
Your job is to detect the mood of the following sentence.
Reply exactly and only like this: “Mood: <Emotion>” (no extra words).
It can be up to two emotions, separated by “/”.
Sentence:
“{user_sentence}”
"""
            # Call OpenAI
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=5,
                temperature=0
            )

            # Display result
            mood = response.choices[0].text.strip()
            st.success(mood)

            # Increment and save count
            usage_data["count"] += 1
            with open(USAGE_FILE, "w") as f:
                json.dump(usage_data, f)

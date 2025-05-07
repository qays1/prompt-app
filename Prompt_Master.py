import streamlit as st
import requests
import os

# Replace with your real API key
API_KEY = "AIzaSyBqf7olH9HJ4Eu11RGeI9EpcrXINm9-cME"

st.set_page_config(page_title="BROKE Prompt Engineer", layout="centered")

st.title("🧠 Prompt Structurer using BROKE Framework")
st.write("Turn vague prompts into clear, structured ones using the BROKE method (Be Specific, Role, Output, Knowledge, Example).")

prompt_input = st.text_area("✍️ Enter your vague prompt here:", height=150)

if st.button("🔧 Generate Structured Prompt"):
    if not prompt_input.strip():
        st.warning("Please enter a prompt.")
    else:
        # Corrected API endpoint for Gemini 2.5
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": f"""
Here is a vague prompt from a user: "{prompt_input}"

Convert it into a BROKE prompt using the same topic. DO NOT change the topic. Only clarify and structure it.

Respond ONLY in the following format:

### BROKE Structured Prompt

**B - Be Specific:**
...

**R - Role Assignment:**
...

**O - Output Format:**
...

**K - Knowledge Context:**
...

**E - Example Prompt:**
...
"""
                        }
                    ]
                }
            ]
        }

        # Call Gemini 2.5 API
        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            try:
                reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.success("🎉 Structured Prompt Generated:")
                st.markdown(reply)
            except KeyError:
                st.error("Error: Could not parse Gemini response.")
                st.json(response.json())
        else:
            st.error(f"API Error {response.status_code}:")
            st.json(response.json())

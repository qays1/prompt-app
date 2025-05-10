import streamlit as st
import requests

# Replace with your real API key
API_KEY = "AIzaSyBqf7olH9HJ4Eu11RGeI9EpcrXINm9-cME"

st.set_page_config(page_title="Prompt Engineer: BROKE / CRISPE", layout="centered")

st.title("🧠 Prompt Structurer (BROKE / CRISPE)")
st.write("Structure vague prompts using the BROKE or CRISPE framework — in English or Arabic.")

# Just print mode
just_print_mode = st.checkbox("📄 I already have a structured prompt. Just print it.")

if just_print_mode:
    structured_input = st.text_area("📥 Paste your structured prompt:", height=300)
    if st.button("🖨️ Print Structured Prompt"):
        if not structured_input.strip():
            st.warning("Please paste your structured content.")
        else:
            endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": f"""
Print this structured content clearly as-is, without modifying or summarizing anything. Maintain formatting and headings.

Respond in Arabic if the text is Arabic, or English if it is English.

Structured Content:
{structured_input}
"""
                            }
                        ]
                    }
                ]
            }

            response = requests.post(endpoint, headers=headers, json=data)
            if response.status_code == 200:
                try:
                    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("📋 Printed Structured Prompt:")
                    st.markdown(reply)
                except KeyError:
                    st.error("❌ Could not parse Gemini response.")
                    st.json(response.json())
            else:
                st.error(f"API Error {response.status_code}:")
                st.json(response.json())

else:
    # Language selection
    language = st.selectbox("🌐 Choose Output Language:", ["English", "Arabic"])

    # Framework selection
    framework_options = st.multiselect(
        "🧩 Choose Framework(s):",
        options=["BROKE", "CRISPE"],
        default=["BROKE"]
    )

    # Detail level
    output_detail = st.radio(
        "🧪 What would you like to see?",
        options=["Only the Example Prompt", "Full Framework Reasoning + Example Prompt"],
        index=0
    )

    # Prompt input
    prompt_input = st.text_area("✍️ Enter your vague prompt here:", height=150)

    # Generate button
    if st.button("🔧 Generate Structured Prompt"):
        if not prompt_input.strip():
            st.warning("Please enter a prompt.")
        elif not framework_options:
            st.warning("Please select at least one framework.")
        else:
            # Build framework instruction
            framework_instruction = ""

            for framework in framework_options:
                if framework == "BROKE":
                    framework_instruction += "\nUse the BROKE framework:\n\n"
                    if output_detail == "Only the Example Prompt":
                        framework_instruction += "Only include the 'Example Prompt' section from the BROKE framework.\n"
                    else:
                        framework_instruction += """
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
                elif framework == "CRISPE":
                    framework_instruction += "\nUse the CRISPE framework:\n\n"
                    if output_detail == "Only the Example Prompt":
                        framework_instruction += "Only include the 'Example Prompt' section from the CRISPE framework.\n"
                    else:
                        framework_instruction += """
### CRISPE Structured Prompt

**C - Context:**
...

**R - Role:**
...

**I - Input:**
...

**S - Steps:**
...

**P - Parameters:**
...

**E - Example Prompt:**
...
"""

            # Add language request
            if language == "Arabic":
                framework_instruction += "\nRespond in Arabic."
            else:
                framework_instruction += "\nRespond in English."

            # Prepare Gemini API request
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

{framework_instruction}
"""
                            }
                        ]
                    }
                ]
            }

            # Call Gemini
            response = requests.post(endpoint, headers=headers, json=data)

            if response.status_code == 200:
                try:
                    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("🎉 Generated Prompt(s):")
                    st.markdown(reply)
                except KeyError:
                    st.error("❌ Could not parse Gemini response.")
                    st.json(response.json())
            else:
                st.error(f"API Error {response.status_code}:")
                st.json(response.json())

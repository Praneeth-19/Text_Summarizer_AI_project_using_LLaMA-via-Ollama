import streamlit as st
import requests

st.title("LLaMA Text Summarizer")
user_input = st.text_area("Enter your text here:")

if st.button("Summarize"):
    try:
        # Modified to use form-encoded data properly
        response = requests.post(
            "http://localhost:8000/summarize/",
            data={"text": user_input},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        summary = response.json().get("summary", "Error generating summary.")
        st.subheader("Summary:")
        st.write(summary)
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
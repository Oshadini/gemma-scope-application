import streamlit as st
import requests
import re  # For tokenization

# Constants
API_URL = "https://www.neuronpedia.org/api/search-all"
HEADERS = {
    "Content-Type": "application/json",
    "X-Api-Key": "your_api_key_here"  # Replace with your actual API token
}

# Helper Function: Tokenize sentence
def tokenize_sentence(sentence):
    """Tokenize the input sentence into words or punctuation."""
    return re.findall(r"\b\w+\b|[^\w\s]", sentence)

# Helper Function: Fetch explanations from API
def fetch_descriptions(token):
    """Fetch descriptions for a given token from the API."""
    payload = {"text": token}
    explanations = []
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        result_data = response.json().get("result", [])
        
        # Extract nested descriptions
        for result in result_data:
            neuron = result.get("neuron", {})  # Get 'neuron' object
            if neuron:
                nested_explanations = neuron.get("explanations", [])  # Access 'explanations'
                if isinstance(nested_explanations, list):  # Ensure it's a list
                    for explanation in nested_explanations:
                        explanations.append({
                            "description": explanation.get("description", "No description available"),
                            "neuron": neuron
                        })
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
    return explanations

# Streamlit UI Setup
st.set_page_config(page_title="Token Description Tool", layout="wide")

# User Input via Chat
st.markdown("<h1 style='text-align: center; color: #007acc;'>Token Description Tool</h1>", unsafe_allow_html=True)
user_input = st.chat_input("Your Message:", key="user_input")

if user_input:
    # Tokenize the sentence
    tokens = tokenize_sentence(user_input)
    
    # Fetch descriptions for each token
    token_descriptions = {}
    for token in tokens:
        descriptions = fetch_descriptions(token)
        token_descriptions[token] = descriptions
    
    # Display Results
    st.markdown("<h2 style='color: #007acc;'>Generated Descriptions</h2>", unsafe_allow_html=True)
    for token, descriptions in token_descriptions.items():
        if descriptions:
            st.markdown(f"**Token: `{token}`**", unsafe_allow_html=True)
            for desc in descriptions:
                neuron = desc.get("neuron", {})
                st.markdown(
                    f"<div style='background-color: #f0f8ff; border-radius: 5px; padding: 10px; margin: 5px 0;'>"
                    f"<strong>Neuron:</strong> {neuron.get('name', 'Unknown')}<br>"
                    f"{desc.get('description', 'No description available')}"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.markdown(f"**Token: `{token}` - No descriptions found.**", unsafe_allow_html=True)

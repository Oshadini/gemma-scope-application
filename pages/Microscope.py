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
    payload = {
        "modelId": "gpt2-small",
        "sourceSet": "res-jb",
        "text": token,  # Use the token here
        "selectedLayers": ["6-res-jb"],
        "sortIndexes": [1],
        "ignoreBos": False,
        "densityThreshold": -1,
        "numResults": 50
    }
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

# UI Header
st.markdown("<h1 style='text-align: center; color: #007acc;'>Token Description Tool</h1>", unsafe_allow_html=True)

# Initialize session state for tokens and selected token
if "tokens" not in st.session_state:
    st.session_state["tokens"] = []
if "selected_token" not in st.session_state:
    st.session_state["selected_token"] = None

# User Input via Chat
user_input = st.chat_input("Your Message:", key="user_input")

if user_input:
    # Tokenize the sentence and store tokens in session state
    st.session_state["tokens"] = tokenize_sentence(user_input)

# Display tokens as selectable buttons
if st.session_state["tokens"]:
    st.markdown("<h3 style='color: #007acc;'>Generated Tokens</h3>", unsafe_allow_html=True)
    cols = st.columns(len(st.session_state["tokens"]))
    for idx, token in enumerate(st.session_state["tokens"]):
        if cols[idx].button(token):
            st.session_state["selected_token"] = token  # Store selected token in session state

# Display descriptions for the selected token
if st.session_state["selected_token"]:
    selected_token = st.session_state["selected_token"]
    st.markdown(f"<h3 style='color: #007acc;'>Descriptions for Token: `{selected_token}`</h3>", unsafe_allow_html=True)
    descriptions = fetch_descriptions(selected_token)
    
    if descriptions:
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
        st.markdown(f"No descriptions found for `{selected_token}`.", unsafe_allow_html=True)

import streamlit as st
import requests

# Streamlit UI
st.title("Neuronpedia API Tester")
st.markdown("Enter the details below to test the API.")

# Input fields
api_key = st.text_input("API Key", type="password")
model_id = st.text_input("Model ID", value="gpt2-small")
source_set = st.text_input("Source Set", value="res-jb")
text_input = st.text_area("Text Input", value="hello world")
selected_layers = st.text_input("Selected Layers (comma-separated)", value="6-res-jb")
sort_indexes = st.text_input("Sort Indexes (comma-separated)", value="1")
ignore_bos = st.checkbox("Ignore BOS", value=False)
density_threshold = st.number_input("Density Threshold", value=-1)
num_results = st.number_input("Number of Results", value=50, step=1)

# Send API request on button click
if st.button("Send Request"):
    url = "https://www.neuronpedia.org/api/search-all"
    
    # Prepare payload
    payload = {
        "modelId": model_id,
        "sourceSet": source_set,
        "text": text_input,
        "selectedLayers": selected_layers.split(","),
        "sortIndexes": [int(i) for i in sort_indexes.split(",")],
        "ignoreBos": ignore_bos,
        "densityThreshold": density_threshold,
        "numResults": num_results
    }
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    
    # Make the POST request
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            st.success("Request Successful!")
            st.json(response.json())
        else:
            st.error(f"Request failed with status code {response.status_code}")
            st.text(response.text)
    except Exception as e:
        st.error("An error occurred!")
        st.text(str(e))

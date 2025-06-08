#!/bin/bash

# Start the Ollama server in the background
ollama serve &

# Wait a little to ensure Ollama starts up properly
sleep 5

# Start the Streamlit app
streamlit run app.py --server.port=80 --server.address=0.0.0.0

# GenAI Storyteller

A Streamlit app that generates 4-scene illustrated stories using Falcon-7B-Instruct and Stable Diffusion (Hugging Face API).

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Replace HF_TOKEN in `utils/hf_api.py` with your Hugging Face token
4. Run the app: `streamlit run app.py`

## Features
- Input a starting sentence
- Generates a 4-scene story
- Generates images for each scene

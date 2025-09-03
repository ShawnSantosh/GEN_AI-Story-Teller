# app.py
# -*- coding: utf-8 -*-

import streamlit as st
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import your custom functions from the utils directory
from utils.hf_api import query_gemini, query_sd
from utils.parser import parse_story_markdown

def generate_story_and_images(start_sentence):
    """
    Generates a 4-scene story using Gemini and images using Stable Diffusion.
    """
    # This prompt is now specifically for the Gemini model
    instruction = f"""
You are a creative storyteller. Your task is to expand the user's idea into a 4-scene illustrated short story.
Each scene must strictly follow this Markdown structure without any deviation:

Scene 1: The Opening
Story:
[A single, well-written paragraph setting the scene.]

Image Prompt:
[A concise, descriptive prompt for an AI image generator, focusing on visual details.]

Scene 2: The Inciting Incident
Story:
[A single paragraph where the main conflict or event begins.]

Image Prompt:
[A concise visual description for this scene.]

Scene 3: The Climax
Story:
[A single paragraph describing the peak of the action or tension.]

Image Prompt:
[A concise visual description for this scene.]

Scene 4: The Resolution
Story:
[A single paragraph that concludes the story and resolves the conflict.]

Image Prompt:
[A concise visual description for this final scene.]

---
User's Starting Idea: "{start_sentence}"
"""
    # Call the Gemini API to get the story text
    story_text = query_gemini(instruction)
    
    if not story_text:
        st.error("Story generation failed. The API might be busy.")
        return []

    scenes = parse_story_markdown(story_text)

    # The rest of the logic for parallel image generation remains the same
    scenes_with_index = [{"index": i, **scene} for i, scene in enumerate(scenes)]
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_scene = {executor.submit(query_sd, s['prompt']): s for s in scenes_with_index}
        for future in as_completed(future_to_scene):
            scene = future_to_scene[future]
            try:
                img = future.result()
            except Exception as e:
                img = None
                st.error(f"Image generation failed for '{scene['title']}': {e}")
            
            results.append({
                "index": scene['index'],
                "title": scene['title'],
                "story": scene['story'],
                "image": img
            })

    results.sort(key=lambda x: x['index'])
    return results

# --- Streamlit UI ---
st.set_page_config(page_title="GenAI Storyteller", layout="wide")
st.title("GenAI Storyteller with Gemini & Stable Diffusion")
st.write("Enter a starting sentence and generate a 4-scene illustrated story.")

start_sentence = st.text_input("Starting Sentence", "", placeholder="A lone astronaut discovers a strange, glowing plant on Mars...")

if st.button("Generate Story"):
    if start_sentence.strip():
        with st.spinner("✍️ Generating story with Gemini..."):
            scenes = generate_story_and_images(start_sentence)
        
        if not scenes:
            st.warning("Could not generate the story. Please try a different starting sentence.")
        else:
            for scene in scenes:
                st.subheader(f"{scene['title']}")
                st.write(scene["story"])
                if scene["image"]:
                    st.image(scene["image"], use_column_width=True)
                else:
                    st.warning("Image could not be generated for this scene.")
    else:
        st.warning("Please enter a starting sentence.")
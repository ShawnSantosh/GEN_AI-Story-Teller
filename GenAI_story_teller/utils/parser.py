# utils/parser.py

import re

def parse_story_markdown(story_text: str):
    """
    Parses the Markdown-formatted story text from the LLM into a list of scene dictionaries.
    """
    scenes = []
    # This regex is designed to be robust and capture all parts of each scene
    pattern = r"Scene \d+:\s*(.*?)\s*\n+Story:\s*\n(.*?)\s*\n+Image Prompt:\s*\n(.*?)(?=\n+Scene \d+:|\Z)"
    matches = re.findall(pattern, story_text, re.DOTALL)

    for title, story, prompt in matches:
        scenes.append({
            "title": title.strip(),
            "story": story.strip(),
            "prompt": prompt.strip()
        })
    return scenes
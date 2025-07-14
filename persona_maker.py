import os
import json
import glob
from google import genai
from dotenv import load_dotenv
load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv('GEMINI_API_KEY')
llm = genai.Client(api_key=API_KEY)

# --- Build Prompt Function ---
def build_prompt(data, max_items=25):
    prompt = (
        "You are an expert behavioral analyst.\n"
        "Given the following Reddit activity (posts and comments), generate a detailed user persona.\n"
        "For each trait (interest, tone, profession guess, etc.), cite the ID or snippet of the specific post/comment used.\n"
        "Format clearly: list each trait followed by the citation.\n\n"
        "Reddit Activity:\n"
    )
    for i, item in enumerate(data[:max_items], 1):
        prompt += f"\n{i}. ID: {item.get('id', 'N/A')}\n"
        prompt += f"   Type: {item.get('type', 'N/A')}\n"
        prompt += f"   Text: {item.get('text', '')[:500]}...\n"
    return prompt

# --- Loop Through All *_comments.json Files ---
json_files = glob.glob("*_comments.json")

if not json_files:
    print("No *_comments.json files found.")
else:
    for file in json_files:
        try:
            username = file.split("_")[0]
            outfile = f"persona_{username}.txt"

            with open(file, "r", encoding="utf-8") as f:
                reddit_data = json.load(f)

            if not reddit_data:
                print(f"Skipping empty file: {file}")
                continue

            prompt = build_prompt(reddit_data)
            response = llm.models.generate_content(
                model = 'gemini-2.5-flash',
                contents = prompt,
            )

            with open(outfile, "w", encoding="utf-8") as out:
                out.write(response.text)

            print(f"Persona for u/{username} saved to {outfile}")
        except Exception as e:
            print(f"Error processing {file}: {e}")

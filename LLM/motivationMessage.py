import json
import random
import os
def get_random_motivation(emotion):

    model_directory = os.path.join("C:\\Users\\secii\\OneDrive\\Masaüstü\\LLM\\motivationCategories")
    motivation_file_path = os.path.join(model_directory, f'{emotion}.json')
    try:
        with open(motivation_file_path, 'r', encoding='utf-8') as file:
            motivations = json.load(file).get('motivations', [])
        if motivations:
            random_motivation = random.choice(motivations)
            return random_motivation
        else:
            return f"No text was found in the motivation file."
    except FileNotFoundError:
        return f"{emotion.capitalize()} Motivation file not found."


# Image Generation Using OpenAI Dalle-3 Model

"""
Requirements:
Python: (winget install python) for windows only
OpenAI Python Library: (pip install openai)
"""
from openai import OpenAI

# Paste Your OpenAI API key here!
client = OpenAI(api_key="your_openai_api_key")

# Prompt
user_input = "Create an image of a majestic T-Rex in a dense, vibrant forest. Sunlight filters through the canopy, highlighting the T-Rex's detailed scales and sharp teeth. Surround it with prehistoric plants and add creative touches like a distant waterfall or smaller dinosaurs hiding among the trees."

response = client.images.generate(model='dall-e-3', prompt=user_input, size='1024x1024', quality='hd',n=1,style='vivid')
image_url = response.data[0].url
print(image_url)

import openai
import os
from PIL import Image
import base64
import io

# import the OpenAI API key from the env file
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")




# Function to load an image and encode it in base64 format
def load_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert image to bytes
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")  # You can also use JPEG, but PNG is preferred
        img_bytes = buffered.getvalue()

    # Convert image bytes to base64 string
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_base64


# Function to send the image to OpenAI and get caption
def get_image_caption(image_base64):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates captions for images."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please describe this image in great detail."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                ],
            },
        ],
        max_tokens=300,
    )

    response = response.choices[0].message.content.strip()

    # now rewrite the caption to start with 'This is TOK...' using GPT-4
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that rewrites captions."},
            {
                "role": "user",
                "content": f"The person that is described is named TOK, she is a woman. Rewrite the following text by taking into account that his name is TOK. Only respons with the rewritten text: {response}",
            },
        ],
    )
    return response.choices[0].message.content.strip()


folder = "jess"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

image_files = [file for file in os.listdir(folder) if file.endswith(".png") or file.endswith(".jpeg")]

for file in image_files:
    print(file)
    # Path to the image you want to caption
    image_base64 = load_image(folder + "/" + file)
    caption = get_image_caption(image_base64)
    # create a new txt file with the caption
    with open(folder + "/" + file.split(".")[0] + ".txt", "w") as f:
        f.write(caption)
    print(caption)

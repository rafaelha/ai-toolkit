from diffusers import AutoPipelineForText2Image
import torch
from dotenv import load_dotenv
import os
from IPython.display import display
import time


def get_new_path():
    # files are stored as image_1.webp, image_2.webp, etc.
    files = os.listdir()
    files = [f for f in files if f.endswith(".webp")]
    files = sorted(files)
    if len(files) == 0:
        return "image_1.webp"
    else:
        last_file = files[-1]
        last_file = last_file.split(".")[0]
        last_file = last_file.split("_")[-1]
        last_file = int(last_file)
        return f"image_{last_file + 1}.webp"


# Load the .env file if it exists
load_dotenv()


pipeline = AutoPipelineForText2Image.from_pretrained(
    "black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16
).to("cuda")
# pipeline.enable_model_cpu_offload()
# pipeline.load_lora_weights("sayakpaul/yarn_art_lora_flux", weight_name="pytorch_lora_weights.safetensors")



# %%

start = time.perf_counter()

pipeline.load_lora_weights(
    # "rafaelha/test_lora", weight_name="rafa_lora_v1_000002400.safetensors",
    "j_lora_v1_000002000.safetensors",
    cross_attention_kwargs={"scale": 0.0},
)
# prompt = "TOK, a man in his 30th, as an astronaut floating in front of the ISS"
prompt = "Corporate Leader: A male named TOK, Caucasian, with neatly combed dark hair and clean-shaven, wearing a dark suit with a blue tie. He is standing confidently with arms crossed, against a sleek glass office backdrop."
prompt = "Go pro close up view of TOK skydiving by himself with a parachute over Berlin, his hands and legs are spread out, and he is smiling."
prompt = "TOK, a create startup founder is standing in front of blackboard with lots of physics equations. He is 30, clean shaven, has razor thin shaved sides (haircuit), wears a manbun and wears a casual white dess shirt."
prompt = "Studio Portrait with a Soft Smile: A full upper body shot of TOK, a woman with long, wavy blonde hair and blue eyes, standing in a professional studio setting. Her hair falls softly over her shoulders, and she is smiling gently at the camera. She is wearing a gray coat. Blurry scene of office in the background."
images = pipeline(
    prompt,
    guidance_scale=0.0,
    height=1024,
    width=1024,
    num_images_per_prompt=1,
    num_inference_steps=32,
    generator= torch.Generator(device="cuda").manual_seed(936188)
).images
print(f"Time taken: {time.perf_counter() - start:.2f}s")

for image in images:
    display(image)
    path = get_new_path()
    image.save(path)

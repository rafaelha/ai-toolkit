from diffusers import AutoPipelineForText2Image
import torch
from dotenv import load_dotenv
# Load the .env file if it exists
load_dotenv()


pipeline = AutoPipelineForText2Image.from_pretrained(
    "black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16
).to("cuda")
pipeline.enable_model_cpu_offload()
pipeline.load_lora_weights("sayakpaul/yarn_art_lora_flux", weight_name="pytorch_lora_weights.safetensors")
# pipeline.load_lora_weights("rafaelha/test_lora", weight_name="rafa_lora_v1_000002400.safetensors")
image = pipeline("TOK, a man in his 30th, wearing a suit", guidance_scale=3.5, height=768).images[0]
image.save("yarn.png")
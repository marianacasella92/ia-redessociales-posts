import requests, os
from pathlib import Path
from rembg import remove  # opcional

A1111_URL = os.environ.get("A1111_URL", "http://127.0.0.1:7860")

def icon_prompt_from_title(title: str) -> str:
    # Converti a algo breve para el tema del icono
    base = title.lower()
    # Podés simplificar más si querés
    return f"flat vector icon about: {base}, modern clean illustration, centered, minimal, professional, vibrant colors, no text"

def sd_txt2img(prompt: str, negative_prompt: str, out_path: str,
               width=768, height=768, steps=30, cfg=6.5, sampler="DPM++ 2M Karras", seed=0):
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler_name": sampler,
        "seed": seed,
        "batch_size": 1,
    }
    r = requests.post(f"{A1111_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
    r.raise_for_status()
    img_b64 = r.json()["images"][0]
    import base64
    img_bytes = base64.b64decode(img_b64.split(",",1)[-1])
    Path(out_path).write_bytes(img_bytes)

# Opcional: quitar fondo para que el icono se integre mejor
def remove_bg_file(src: str, dst: str):
    from rembg import remove
    data = Path(src).read_bytes()
    Path(dst).write_bytes(remove(data))

def generate_icon_if_needed(title: str, out_dir: str) -> str:
    icon_png = os.path.join(out_dir, "icon.png")
    icon_cut = os.path.join(out_dir, "icon_cut.png")
    if not os.path.exists(icon_png):
        prompt = icon_prompt_from_title(title)
        neg = "photo, photorealistic, text, watermark, low quality, blur, background pattern"
        sd_txt2img(prompt, neg, icon_png, width=768, height=768, steps=26, cfg=6.5, seed=0)
        # quitar fondo (opcional)
        # remove_bg_file(icon_png, icon_cut)
        # return icon_cut
    return icon_png

import os
import sys
import json
import textwrap
import subprocess
from pathlib import Path
from jinja2 import Template
from flat_icon import generate_icon_if_needed

# ===== Rutas base =====
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT)

TPL_DIR = os.path.join(BASE, "templates")
OUT_BASE = os.path.join(BASE, "out")

# ===== Heurísticas de wrap =====
CHARS_PER_LINE_TITLE = 20
CHARS_PER_LINE_BULLET = 40

# ===== Utilidades =====
def wrap_lines(text: str, width_chars: int):
    text = (text or "").strip()
    lines = textwrap.wrap(text, width=width_chars)
    return lines

def render_svg(template_path: str, context: dict, dst_svg: str):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = Template(f.read())
    svg = tpl.render(**context)
    with open(dst_svg, "w", encoding="utf-8") as f:
        f.write(svg)

def export_png(src_svg: str, dst_png: str):
    subprocess.run([
        "inkscape",
        src_svg,
        "--export-type=png",
        f"--export-filename={dst_png}"
    ], check=True)

def pick_idea(ideas: list, idea_id: int) -> dict:
    for it in ideas:
        if it.get("id") == idea_id:
            return it
    raise ValueError(f"ID no encontrado: {idea_id}")

# ===== Contextos para las plantillas =====
def to_title_context(title: str):
    title = (title or "").upper()
    lines = wrap_lines(title, CHARS_PER_LINE_TITLE)
    while len(lines) < 3:
        lines.append("")
    return {
        "TITLE_LINE1": lines[0],
        "TITLE_LINE2": lines[1],
        "TITLE_LINE3": lines[2],
    }

def bullets_to_lines(bullets: list, width_chars: int = CHARS_PER_LINE_BULLET,
                     max_lines: int = 3, max_items: int = 5):
    out = []
    for b in bullets[:max_items]:
        lines = wrap_lines(b, width_chars)[:max_lines]
        while len(lines) < max_lines:
            lines.append("")
        out.append({"LINE1": lines[0], "LINE2": lines[1], "LINE3": lines[2]})
    return out

def to_interna_list_context(title: str, bullets: list):
    title = (title or "").upper()
    tlines = wrap_lines(title, CHARS_PER_LINE_TITLE)[:2]
    while len(tlines) < 2:
        tlines.append("")
    return {
        "TITLE_LINE1": tlines[0],
        "TITLE_LINE2": tlines[1],
        "BULLETS": bullets_to_lines(bullets)
    }

def to_cta_context(cta: str):
    lines = wrap_lines(cta, CHARS_PER_LINE_BULLET)
    while len(lines) < 3:
        lines.append("")
    return {
        "CTA_LINE1": lines[0],
        "CTA_LINE2": lines[1],
        "CTA_LINE3": lines[2],
    }

# ===== Flujo principal =====
def main(idea_id: int, ideas: list):
    idea = pick_idea(ideas, idea_id)

    out_dir = os.path.join(OUT_BASE, f"idea-{idea_id:02d}")
    os.makedirs(out_dir, exist_ok=True)

    # ----- Portada -----
    icon_path = generate_icon_if_needed(idea.get("titulo", ""), out_dir)
    cover_ctx = to_title_context(idea.get("titulo", ""))
    cover_ctx["ICON_PATH"] = icon_path
    render_svg(os.path.join(TPL_DIR, "portada.svg"), cover_ctx, os.path.join(out_dir, "01_portada.svg"))
    export_png(os.path.join(out_dir, "01_portada.svg"), os.path.join(out_dir, "01_portada.png"))


    # ----- Portada -----
    cover_ctx = to_title_context(idea.get("titulo", ""))
    render_svg(os.path.join(TPL_DIR, "portada.svg"),
               cover_ctx,
               os.path.join(out_dir, "01_portada.svg"))
    export_png(os.path.join(out_dir, "01_portada.svg"),
               os.path.join(out_dir, "01_portada.png"))

    # ----- Interna lista -----
    interna_ctx = to_interna_list_context(idea.get("titulo", ""), idea.get("bullets", []))
    render_svg(os.path.join(TPL_DIR, "interna-lista.svg"),
               interna_ctx,
               os.path.join(out_dir, "02_interna.svg"))
    export_png(os.path.join(out_dir, "02_interna.svg"),
               os.path.join(out_dir, "02_interna.png"))

    print(f"✅ Listo: {out_dir}")

# ===== Entrada CLI =====
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python build.py <id_idea> <archivo.json>")
        sys.exit(1)

    idea_id = int(sys.argv[1])
    ideas_file = Path(BASE) / "ideas" / sys.argv[2]

    if not ideas_file.exists():
        print(f"El archivo {ideas_file} no existe.")
        sys.exit(1)

    with open(ideas_file, "r", encoding="utf-8") as f:
        ideas = json.load(f)

    print(f"Generando post con idea: {next((i['titulo'] for i in ideas if i.get('id') == idea_id), '(sin titulo)')}")
    main(idea_id, ideas)

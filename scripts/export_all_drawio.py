#!/usr/bin/env python3
"""
Batch export all 24 draw.io diagrams to high-resolution PNG and SVG
using the official draw.io CLI.
"""

import os
import subprocess
import glob

DRAWIO_DIR = "docs/diagrams/drawio"
PNG_DIR = "docs/diagrams/png"
SVG_DIR = "docs/diagrams/svg"
DRAWIO_BIN = "/home/sathvik/.local/bin/drawio"

os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(SVG_DIR, exist_ok=True)

files = sorted(glob.glob(os.path.join(DRAWIO_DIR, "*.drawio")))
print(f"Found {len(files)} draw.io files to export.\n")

success_png = 0
success_svg = 0

for f in files:
    base = os.path.splitext(os.path.basename(f))[0]
    out_png = os.path.join(PNG_DIR, f"{base}.png")
    out_svg = os.path.join(SVG_DIR, f"{base}.svg")
    
    # Export PNG
    cmd_png = [DRAWIO_BIN, "--no-sandbox", "-x", "-f", "png", "--scale", "2", "-o", out_png, f]
    res_png = subprocess.run(cmd_png, capture_output=True, text=True)
    if res_png.returncode == 0 and os.path.exists(out_png) and os.path.getsize(out_png) > 0:
        print(f"  [PNG OK]  {base}.png ({os.path.getsize(out_png)} bytes)")
        success_png += 1
    else:
        print(f"  [PNG ERR] {base}.png: {res_png.stderr}")
        
    # Export SVG
    cmd_svg = [DRAWIO_BIN, "--no-sandbox", "-x", "-f", "svg", "-o", out_svg, f]
    res_svg = subprocess.run(cmd_svg, capture_output=True, text=True)
    if res_svg.returncode == 0 and os.path.exists(out_svg) and os.path.getsize(out_svg) > 0:
        print(f"  [SVG OK]  {base}.svg ({os.path.getsize(out_svg)} bytes)")
        success_svg += 1
    else:
        print(f"  [SVG ERR] {base}.svg: {res_svg.stderr}")

print(f"\nExport complete: {success_png}/24 PNGs, {success_svg}/24 SVGs generated successfully.")

#!/usr/bin/env python3
"""news-image-20261120 entry: copy the pre-built image to /output/entry.png.

The image is a one-page visual newspaper cover summing up the world news
of Friday 20 November 2026, drawn from code (see build_image.py) and
shipped beside this file. A byte copy is deterministic: two runs write
identical bytes. Standard library only, no network.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
SRC = HERE / "entry.png"

if not SRC.is_file():
    raise SystemExit(f"entry.png not found beside {__file__}")

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, OUT / "entry.png")

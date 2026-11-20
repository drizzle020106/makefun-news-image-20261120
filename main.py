#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

Copies the pre-drawn entry.png (built by draw.py) to the output
directory the harness provides. Standard library only, deterministic.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, os.path.join(OUT, "entry.png"))
print("entry.png ok")

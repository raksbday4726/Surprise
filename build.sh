#!/usr/bin/env bash
# Render build script
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Crop favicon to make it fuller in browser tabs
python render_crop_favicon.py

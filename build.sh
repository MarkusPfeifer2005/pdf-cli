#!/bin/bash

python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
pyinstaller --onefile pdf-cli.py
deactivate

#!/bin/bash
virtualenv .venv
source .venv/bin/activate

pip install --upgrade pip --no-cache-dir --break-system-packages
pip install -r requirements.txt --break-system-packages

bash kill.sh 5001 || exit 0

python3 app.py &
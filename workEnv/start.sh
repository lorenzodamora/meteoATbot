#!/bin/bash
project_path="/home/ubuntu/Magnus/PycharmProj/persone/Adora/meteobot"
cd "${project_path}"
source "${project_path}/.python_venv/bin/activate"
cd "workEnv"
python -u mMain.py >> ../output.txt 2>&1

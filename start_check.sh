#!/bin/bash
project_path="/home/ubuntu/Magnus/PycharmProj/persone/Adora/meteobot"
cd "${project_path}"
source "${project_path}/.python_venv/bin/activate"
python -u check_output_4.py &
deactivate

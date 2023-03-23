# certIZDAT-web

## Running

    python3 -m venv env
    source env/bin/activate
    pip3 install -r requirements.txt 
    cd backend/
    bash
    gunicorn app:app --workers=$((2 * $(getconf _NPROCESSORS_ONLN))) --bind 0.0.0.0:80

## Setup crontab configuration for analyser

TODO: add config

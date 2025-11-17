## ENV
# Create a virtual environment in the project folder
python -m venv .venv
# Activate it (Windows)
.venv\Scripts\activate
# Bash
source .venv/Scripts/activate
# Install packages
pip install -r backend/requirements.txt

## Docker
# start docker 
docker-compose up -d

## FastAPI
# start API
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
http://127.0.0.1:8000/docs

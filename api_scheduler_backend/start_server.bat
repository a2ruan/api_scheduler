pip install -r requirements.txt
python -m uvicorn dpq_engine:app --host 0.0.0.0 --port 5000 --reload
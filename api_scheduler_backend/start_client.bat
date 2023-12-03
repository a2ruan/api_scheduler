pip install -r requirements.txt
python -m uvicorn dpq_client:app --host 0.0.0.0 --port 5543 --reload
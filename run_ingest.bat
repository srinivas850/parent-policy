@echo off
REM Activate virtual environment if exists
IF EXIST venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Install requirements
pip install -r requirements.txt

REM Run the ingestion script
python ingest_data.py

echo Ingestion complete. You can now run test_query.py to test the knowledge base.
pause

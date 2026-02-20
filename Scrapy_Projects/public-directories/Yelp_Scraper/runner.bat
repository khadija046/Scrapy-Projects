@echo off
:: Check if venv exists, if not create it
if not exist venv (
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

pip install -r requirements.txt

:: Run Scrapy spider
python main.py

:: Pause to keep the window open
pause
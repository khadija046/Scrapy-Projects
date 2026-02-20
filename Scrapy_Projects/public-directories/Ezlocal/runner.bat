@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install scrapy tkinter

echo Running the Scrapy spider...
scrapy crawl ezlocal

echo Done!
pause

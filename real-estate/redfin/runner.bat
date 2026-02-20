@echo off
:: Check if venv exists, if not create it
if not exist venv (
    python -m venv venv
)

:: Activate the virtual environment
call venv\Scripts\activate

:: Run Scrapy spider
scrapy crawl redfin_agents

:: Pause to keep the window open
pause
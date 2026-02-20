Ahh got it 👍 — **this README is for your Selenium + Yelp desktop scraper**, **NOT Scrapy / Zyte / Google Sheets**.

Below is a **clean, professional `README.md`** tailored **exactly** to your **Yelp Selenium + Tkinter project**, including:

* What the scraper does
* Windows & macOS run instructions
* `runner.bat` (Windows)
* `requirements.txt`
* Project structure
* Notes about manual interaction & pagination

No Scrapy. No Zyte. No cloud. Pure Selenium + GUI.

You can copy-paste this directly.

---

# Yelp Business Scraper (Selenium + Tkinter)

This project is a **desktop-based Yelp scraper** built with **Selenium**, **Undetected ChromeDriver**, and **Tkinter**.

It allows you to:

* Open Yelp safely (captcha-friendly)
* Manually enter **search keyword & location**
* Scrape business names and websites
* Control pagination using **GUI dialogs**
* Watch live scraper status in the terminal
* Save results to a CSV file

This scraper is designed for **interactive, human-assisted scraping**, not headless automation.

---

## 📁 Project Structure

```text
yelp_scraper/
│
├── app.py                 # Tkinter dialogs & shared utilities
├── scraper.py             # Main Selenium scraper
├── runner.bat             # Windows runner
├── requirements.txt       # Python dependencies
├── output/
│   └── Yelp_data.csv      # Scraped results
└── README.md
```

---

## ⚙️ Requirements

### System

* Windows 10 / 11 **or** macOS
* Google Chrome (latest)
* Python **3.9+**

### Python Dependencies

`requirements.txt`

```txt
selenium
undetected-chromedriver
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How the Scraper Works

1. Opens Google
2. Searches for `yelp.com`
3. Opens Yelp homepage
4. **Pauses** and waits for the user to:

   * Enter keyword (e.g. restaurants)
   * Enter location (e.g. New York)
5. Scraper resumes
6. For each business:

   * Opens listing in a new tab
   * Extracts business name
   * Extracts website (if available)
   * Saves data to CSV
7. If more pages exist:

   * Shows a **GUI confirmation dialog**
   * User decides whether to continue

---

## ▶️ Running the Scraper

---

### 🪟 Windows (Recommended)

#### 1️⃣ Install dependencies

```bat
pip install -r requirements.txt
```

#### 2️⃣ Run using `runner.bat`

```bat
runner.bat
```

#### Example `runner.bat`

```bat
@echo off
python main.py
pause
```

This keeps the terminal open and shows live scraper logs.

---

### 🍎 macOS / Linux

#### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 2️⃣ Run scraper

```bash
python main.py
```

---

## 🖥️ GUI Dialogs Used

### ⏸ Pause Dialog

* Appears after Yelp opens
* Allows user to enter keyword & location
* Click **Restart Scraper** to continue

### 📄 Pagination Dialog

* Appears when a next page is detected
* User chooses:

  * **Continue** → scrape next page
  * **Stop Scraper** → exit gracefully

---

## 📊 Output

Data is written to:

```text
output/Yelp_data.csv
```

Example columns:

| restaurantName | websiteUrl                                     |
| -------------- | ---------------------------------------------- |
| Joe’s Pizza    | [https://joespizza.com](https://joespizza.com) |
| Sushi Zen      |                                                |

The CSV **auto-expands** if new fields are added later.

---

## 🧠 Terminal Status Logs

The scraper prints live status updates, including:

* Browser launch
* Page navigation
* Business count per page
* Record extraction
* CSV writes
* Pagination decisions
* Clean shutdown

This makes it easy to **monitor progress in real time**.

---

## ⚠️ Important Notes

* This scraper is **NOT headless**
* Manual interaction is required
* Designed to reduce CAPTCHA risk
* Do **not** run aggressively
* Yelp structure may change over time

---

## 🛠️ Troubleshooting

| Issue              | Solution                         |
| ------------------ | -------------------------------- |
| Chrome not opening | Update Chrome                    |
| Driver error       | Update `undetected-chromedriver` |
| CAPTCHA appears    | Slow down / restart              |
| No data saved      | Check `output/` folder           |
| Script exits early | Check terminal logs              |

---

## 📌 Maintainer Notes

This project is intentionally designed as a **human-assisted scraper**.

Easy future upgrades:

* Auto-pagination mode
* Headless mode toggle
* Proxy support
* Resume from last page
* Tkinter control panel

---

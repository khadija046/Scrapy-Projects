# 🕷️ Multi-Category Web Scraping Framework

A scalable and modular web scraping framework built with **Python, Scrapy, Selenium**, and **Excel/Database exports**.
This project is designed to scrape data from multiple industries including:

* 🛒 E-commerce
* 🏢 Public Directories
* 🏠 Real Estate
* 🌐 Website Extraction
* 🔧 Other Custom Scrapers

The architecture supports reusable spiders, dynamic content handling, pagination, data cleaning, and structured exports.

---

# 📁 Project Structure

```
project-root/
│
├── e-commerce/           # E-commerce spiders
├── public-directories/   # Business directory spiders
├── real-estate/          # Property data spiders
├── WebsitesExtraction/   # Website metadata/content spiders
├── otherScrapers/        # Custom or one-off spiders
│
├── common/               # (optional) shared utilities
├── exports/              # Output files (Excel/CSV)
├── database/             # DB connectors or dumps
├── requirements.txt
└── README.md
```

---

# ⚙️ Features

* Scrapy-based high-performance crawling
* Selenium support for JavaScript-heavy websites
* Modular spider design per category
* Pagination & infinite scroll handling
* Proxy & custom headers support
* Data cleaning and normalization
* Export to:

  * Excel (`.xlsx`)
  * CSV
  * Database (if configured)
* Error handling and logging ready
* Scalable for multiple domains

---

# 🧰 Tech Stack

* Python 3.9+
* Scrapy
* Selenium
* Pandas
* OpenPyXL / XlsxWriter
* SQLite / MySQL / PostgreSQL *(optional based on configuration)*

---

# 🚀 Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

## 2️⃣ Create Virtual Environment

### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 🍎 macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🌐 Selenium Setup

If your spiders use Selenium:

### Install Browser Driver

* Chrome → [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
* Make sure the driver version matches your browser

Place the driver in:

```
/drivers/
```

or add it to your system PATH.

---

# ▶️ Running Spiders

Navigate to the specific category folder and run:

```bash
scrapy crawl spider_name
```

Example:

```bash
cd e-commerce
scrapy crawl products_spider
```

---

# 📤 Output

By default, data is exported to the `exports/` folder:

* Excel → `exports/data.xlsx`
* CSV → `exports/data.csv`

You can also enable database storage inside the pipeline settings.

---

# 🗄️ Database Configuration (Optional)

Update your database credentials in:

```
settings.py or database/config.py
```

Example (SQLite):

```python
DB_URL = "sqlite:///database/data.db"
```

---

# 🧹 Data Processing

The pipeline handles:

* Removing duplicates
* Standardizing fields
* Price formatting
* Null value handling
* Structured schema output

---

# 🛠️ Customization

To add a new scraper:

1. Create a new spider inside the relevant category folder
2. Reuse shared utilities (requests, parsers, pipelines)
3. Configure exports in `settings.py`
4. Run with:

```bash
scrapy crawl new_spider
```

---

# 📊 Use Cases

* Lead generation
* Market research
* Competitor analysis
* Product catalog extraction
* Business directory aggregation

---

# ⚠️ Notes

* Always respect `robots.txt` and website terms of service
* Use appropriate delays and proxy rotation for large crawls
* Selenium should only be used when necessary (JS-heavy pages)

---

# 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

# 📄 License

This project is for educational and research purposes.
Ensure compliance with the target website’s legal policies before running scrapers.
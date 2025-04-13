# 🕷️ US Attorneys Firms Scraper

This project is a Scrapy-based web scraper built to extract detailed information about attorneys from U.S. law firm websites (over 100 firms) . It uses both Scrapy and Playwright to handle dynamic content.

## 📌 Features

- Extracts attorneys' full names, titles, emails, educational background, bios, and office locations.
- Uses Playwright to render JavaScript and extract hidden elements (like email addresses).
- Handles paginated listings and individual profile pages.
- Modular codebase designed for scalability to multiple law firm websites.

## 🛠️ Technologies Used

- [Scrapy](https://scrapy.org/)
- [Playwright](https://playwright.dev/python/)
- Python 3.8+
- XPath/CSS Selectors

## 📄 Example Spider: `armstrongteasdale`

The `armstrongteasdale.py` spider scrapes data from the Armstrong Teasdale law firm's website.

### Extracted Fields

- `first_name`
- `last_name`
- `title`
- `email` (retrieved using Playwright)
- `bio`
- `image`
- `law_school` and `graduation_year`
- `undergraduate_school` and `graduation_year`
- `office`
- `url` (profile page)
- `firm`
- `firm_bio`

## ▶️ Usage

### 1. Install Dependencies

```bash
pip install scrapy playwright
playwright install
````
Note: playwright install installs necessary browser binaries (Chromium, Firefox, WebKit).

### 2.Run Spider
```bash
scrapy crawl spider_name -o spider_name.json
````


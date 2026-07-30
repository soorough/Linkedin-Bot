# Linkedin-Bot

Automated job application bot for LinkedIn — apply to hundreds of Easy Apply jobs while you sleep.

**Python · Selenium · 4 stars**

---

## How it works

1. Define job search criteria (title, location, experience level, remote preference) in `config.yaml`
2. Bot logs into LinkedIn using a session cookie (no password stored after initial login)
3. Searches Easy Apply jobs matching your criteria
4. For each listing: opens the application, fills standard fields (contact info, resume upload, screening questions), and submits
5. Logs every application to a CSV for tracking

---

## Features

- Easy Apply automation — handles multi-step application flows
- Smart form filling — detects field types (text, dropdown, radio, checkbox)
- Duplicate detection — skips jobs already applied to
- Rate limiting — humanized delays to avoid bot detection
- CSV export — track every application with company, role, date, status

---

## Stack

```
Python 3.10+
Selenium WebDriver (Chrome)
undetected-chromedriver
LinkedIn session-cookie auth
PyYAML for config
```

---

## Setup

```bash
git clone https://github.com/soorough/Linkedin-Bot
cd Linkedin-Bot
pip install -r requirements.txt

cp config.example.yaml config.yaml
# Edit config.yaml with your search criteria

python main.py
```

---

## Config

```yaml
job_search:
  keywords: ["Backend Engineer", "Full Stack Engineer", "AI Engineer"]
  location: "India"
  remote: true
  experience_level: ["Mid-Senior level"]
  max_applications: 50

resume: /path/to/resume.pdf
```

---

> For educational purposes. Use in accordance with LinkedIn ToS.

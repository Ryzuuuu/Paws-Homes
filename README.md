# 🐾 Paws & Homes

A multi-page pet-adoption website built with **Flask** and **Jinja2** templates. Warm, editorial design (Playfair Display + Inter, amber accent) with pages to browse rescue pets, learn about the shelter and get in touch.

## Pages

| Route | Template | What it shows |
|---|---|---|
| `/` | `templates/index.html` | Landing page: split hero, featured rescues (Hazel, Winston, Charlie) |
| `/adopt` | `templates/adopt.html` | "Meet Our Pets": filter sidebar (species etc.) and pet cards |
| `/about` | `templates/about.html` | About the shelter |
| `/contact` | `templates/contact.html` | Contact form and details |

`templates/navbar.html` is a shared navigation partial included by the pages.

## Run locally

Requires Python 3.9+.

```bash
git clone https://github.com/Ryzuuuu/Paws-Homes.git
cd Paws-Homes
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install flask
python app.py
```

Open http://127.0.0.1:5000. The app starts in Flask debug mode.

## Tech stack

Python · Flask · Jinja2 · HTML · inline CSS · Google Fonts · Unsplash images (loaded from the web, so an internet connection is needed to see photos)

## Current status

This is a front-end focused build:

- Pet cards and the adopt-page filters are static markup, with no JavaScript or database behind them yet.
- The contact form posts to `/submit-contact`, which has no handler in `app.py` yet.

Natural next steps: store pets in a database, make the filters work, and add a route that saves contact messages.

# 🐾 Paws & Homes

[![CI](https://github.com/Ryzuuuu/Paws-Homes/actions/workflows/ci.yml/badge.svg)](https://github.com/Ryzuuuu/Paws-Homes/actions/workflows/ci.yml)

A multi-page pet-adoption website built with **Flask** and **Jinja2** templates. Warm, editorial design (Playfair Display + Inter, amber accent) with pages to browse and filter rescue pets, read about each animal, learn about the shelter and get in touch.

## Features

- **Browse and filter pets.** The Adopt page filters by species, age and size (checkboxes inside a group are OR-ed, different groups are AND-ed) and sorts by newest, oldest or name. The state lives in the query string, so filtered views are shareable links.
- **Home page search.** The hero search sends the chosen species and age straight to the filtered Adopt page.
- **Pet detail pages.** Every pet has a page at `/adopt/<slug>` with photo, facts and bio. Its "Ask about" button opens the contact form with the message pre-filled.
- **Working contact form.** Server-side validation with inline error messages, safe re-display of what the user typed, and a thank-you state after a Post/Redirect/Get round trip. Valid messages are appended to `instance/messages.jsonl`.
- **Shared layout.** One base template and nav partial (with active-page highlighting), a custom 404 page, and responsive layouts down to phone width.

## Tech stack

Python 3.9+ · Flask · Jinja2 · HTML/CSS · Google Fonts · Unsplash images (loaded from the web, so an internet connection is needed to see photos) · pytest · GitHub Actions

## Getting started

```bash
git clone https://github.com/Ryzuuuu/Paws-Homes.git
cd Paws-Homes
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

Debug mode (auto-reload and the interactive debugger) is off by default. Enable it for development with `FLASK_DEBUG=1 python app.py` (PowerShell: `$env:FLASK_DEBUG=1; python app.py`).

## Usage

| Route | What it shows |
|---|---|
| `/` | Landing page: hero search and featured rescues |
| `/adopt` | "Meet Our Pets": filter sidebar, sorting and pet cards. Query parameters: `species`, `age`, `size` (repeatable) and `sort` (`newest`, `oldest`, `name`) |
| `/adopt/<slug>` | A single pet, e.g. `/adopt/hazel` |
| `/about` | About the shelter |
| `/contact` | Contact form and shelter details. `?pet=<slug>` pre-fills the message |
| `/submit-contact` | `POST` endpoint behind the contact form |

Example: `/adopt?species=dog&age=baby&sort=name` lists the puppies, alphabetically.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The suite covers page rendering, filtering and sorting, the pet detail routes and the contact form (validation, escaping and saving). It runs on Python 3.9 and 3.12 in GitHub Actions on every push.

## Project structure

```
app.py               Flask app: routes, contact form validation and storage
pets.py              Sample pet data plus the filter/sort logic
templates/           base.html, navbar.html (partial), one template per page, 404.html
static/css/site.css  Shared page base and navigation styles
tests/               pytest suite
```

## Limitations and next steps

- Pets are sample data in `pets.py`, not a database. Moving them to SQLite/SQLAlchemy would be the natural next step.
- Contact messages are stored in a local file; there is no email delivery, spam protection or CSRF token yet.
- There is no admin interface, authentication or adoption-application workflow.

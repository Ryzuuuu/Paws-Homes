"""Paws & Homes: a small pet-adoption website built with Flask."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

import pets

app = Flask(__name__)
app.add_template_global(pets.image_url)
# Contact messages are appended to this file (one JSON object per line).
app.config['MESSAGES_FILE'] = Path(app.instance_path) / 'messages.jsonl'

SUBJECTS = {
    'adopt': 'I want to adopt a pet',
    'volunteer': 'I want to volunteer',
    'donate': 'Donation inquiry',
    'other': 'Other',
}
MAX_MESSAGE_LENGTH = 2000
EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def _selected(name, allowed):
    """Return the valid values of a repeated query parameter, ignoring unknown ones."""
    return [value for value in request.args.getlist(name) if value in allowed]


@app.route('/')
def index():
    return render_template('index.html', featured=pets.PETS[:3],
                           species=pets.SPECIES, age_groups=pets.AGE_GROUPS)


@app.route('/about')
def about():
    return render_template('about.html')


def _render_contact(form, errors=None, sent=False, status=200):
    return render_template('contact.html', form=form, errors=errors or {}, sent=sent,
                           subjects=SUBJECTS, max_message=MAX_MESSAGE_LENGTH), status


def validate_contact(form):
    """Return a dict of field name -> error message (empty if the form is valid)."""
    errors = {}
    if not form['name']:
        errors['name'] = 'Please enter your name.'
    elif len(form['name']) > 100:
        errors['name'] = 'Please keep your name under 100 characters.'
    if not EMAIL_PATTERN.match(form['email']) or len(form['email']) > 254:
        errors['email'] = 'Please enter a valid email address.'
    if form['subject'] not in SUBJECTS:
        errors['subject'] = 'Please choose a subject.'
    if not form['message']:
        errors['message'] = 'Please enter a message.'
    elif len(form['message']) > MAX_MESSAGE_LENGTH:
        errors['message'] = f'Please keep your message under {MAX_MESSAGE_LENGTH} characters.'
    return errors


def save_message(form):
    """Append a contact message to the messages file."""
    path = Path(app.config['MESSAGES_FILE'])
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {'received': datetime.now(timezone.utc).isoformat(timespec='seconds'), **form}
    with path.open('a', encoding='utf-8') as file:
        file.write(json.dumps(record) + '\n')


@app.route('/contact')
def contact():
    form = {'name': '', 'email': '', 'subject': 'adopt', 'message': ''}
    pet = pets.get_pet(request.args.get('pet', ''))
    if pet:  # arriving from a pet page: pre-fill the enquiry
        form['message'] = f"Hi, I'd like to know more about {pet['name']}."
    return _render_contact(form, sent=request.args.get('sent') == '1')


@app.post('/submit-contact')
def submit_contact():
    form = {field: request.form.get(field, '').strip()
            for field in ('name', 'email', 'subject', 'message')}
    errors = validate_contact(form)
    if errors:
        return _render_contact(form, errors, status=400)
    try:
        save_message(form)
    except OSError:
        app.logger.exception('Could not save contact message')
        return _render_contact(
            form, {'message': 'Sorry, we could not send your message. Please try again later.'},
            status=500)
    return redirect(url_for('contact', sent=1))


@app.route('/adopt')
def adopt():
    sort = request.args.get('sort', 'newest')
    if sort not in pets.SORTS:
        sort = 'newest'
    selected = {
        'species': _selected('species', pets.SPECIES),
        'age': _selected('age', pets.AGE_GROUPS),
        'size': _selected('size', pets.SIZES),
    }
    results = pets.search_pets(selected['species'], selected['age'], selected['size'], sort)
    return render_template(
        'adopt.html', pets=results, total=len(pets.PETS), selected=selected, sort=sort,
        species=pets.SPECIES, age_groups=pets.AGE_GROUPS, sizes=pets.SIZES, sorts=pets.SORTS,
        species_counts=pets.count_by('species'), age_counts=pets.count_by('age_group'),
        size_counts=pets.count_by('size'),
    )


@app.route('/adopt/<slug>')
def pet_detail(slug):
    pet = pets.get_pet(slug)
    if pet is None:
        abort(404)
    return render_template('pet.html', pet=pet)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Debug mode is opt-in: set FLASK_DEBUG=1 to enable the reloader and debugger.
    app.run()

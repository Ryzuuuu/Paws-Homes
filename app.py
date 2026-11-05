"""Paws & Homes: a small pet-adoption website built with Flask."""
from flask import Flask, abort, render_template, request

import pets

app = Flask(__name__)
app.add_template_global(pets.image_url)


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


@app.route('/contact')
def contact():
    return render_template('contact.html')


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

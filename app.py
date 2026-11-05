"""Paws & Homes: a small pet-adoption website built with Flask."""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/adopt')
def adopt():
    return render_template('adopt.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Debug mode is opt-in: set FLASK_DEBUG=1 to enable the reloader and debugger.
    app.run()

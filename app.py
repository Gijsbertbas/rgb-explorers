#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, json
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
import processing
import processing.triplets
import processing.rgb_blending

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/generate_triplets', methods = ['POST'])
def generate_triplets():
    """
    Returns the list of triplets.

    Test with:
    curl -X POST --header "Content-Type: application/json" --data '{"hello":"world"}' http://localhost:5000/generate_triplets

    For the moment data is not used.
    :return: The list of triplets.
    """
    body = json.loads(request.data)
    # Be careful the link is synchronous
    triplets = processing.triplets.generate_triplets()
    return json.jsonify(triplets)

@app.route('/rgb_blending', methods = ['POST'])
def rgb_blending():
    """
    Compute the rbg blendings for all the triplets from the data body.

    Test with:
    curl -X POST --header "Content-Type: application/json" --data '[[1, 2, 3],[1.0, 3.3, 5],[1.0, 7, 15]]' http://localhost:5000/rbg_blending
    Be careful no to forget the trailing 0 when sending floats.

    For the moment data is not used.
    :return: "Done"
    """
    # data in string format and you have to parse into dictionary
    rgbs = json.loads(request.data)
    # Be careful the link is synchronous
    map(processing.rgb_blending.compute, rgbs)
    return "Done"

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

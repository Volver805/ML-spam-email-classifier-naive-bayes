import os
from Classifier import Classifier
from flask import (
    Flask, render_template, request, redirect, url_for, session
)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    classifier = Classifier('emails.csv')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def welcome():
        prediction = session.get('prediction')
        previousEmail = session.get('previousEmail')
        session.clear()
        return render_template('index.html',
                               prediction=prediction,
                               previousEmail=previousEmail
                               )

    @app.route('/predict', methods=['GET', 'POST'])
    def predict():
        subject = session['previousEmail'] = request.form.get('subject')
        session['prediction'] = classifier.predictSpam([subject])
        return redirect('/')

    return app

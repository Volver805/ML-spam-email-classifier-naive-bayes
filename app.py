import os
from Classifier import Classifier
from flask import (
    Flask, render_template, request, redirect, url_for, session
)

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
classifier = Classifier('emails.csv')


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


if __name__ == "__main__":
    app.run(port=5000, debug=True)

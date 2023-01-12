from flask import Flask, request, render_template, redirect, flash, jsonify
from surveys import Survey, Question
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "shiddy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)


survey = Survey("Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?",["Yes", "No"]),
        Question("Did someone else shop with you today?",["Yes", "No"]),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?",["Yes", "No"]),
    ])

responses = {}

@app.route('/')
def home():
    return render_template('home.html', survey = survey)

@app.route('/survey', methods=['GET', 'POST'])
def take_survey():
    current_question = int(request.args.get('question',0))
    if request.method == 'POST':
        responses[current_question] = request.form['response']
        if current_question == len(survey.questions) -1:
            return render_template('responses.html', responses=responses)
        else:
            current_question += 1
            return render_template('survey.html', question=survey.questions[current_question], current_question=current_question)
    else:
         return render_template("survey.html", question=survey.questions[current_question], current_question=current_question)
if __name__ == "__main__":
    app.run(debug=True)


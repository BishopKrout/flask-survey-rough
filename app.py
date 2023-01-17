from flask import Flask, request, render_template, redirect, flash, session, url_for
from surveys import Survey, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = "shiddy"

survey = Survey("Please fill out a survey about your experience with us.",
    [
        Question("Have you shopped here before?",["Yes", "No"]),
        Question("Did someone else shop with you today?",["Yes", "No"]),
        Question("On average, how much do you spend a month on frisbees?",
                 ["Less than $10,000", "$10,000 or more"]),
        Question("Are you likely to shop here again?",["Yes", "No"]),
    ])

session = {}

@app.route('/')
def home():
    return render_template('home.html', survey = survey)

@app.route('/survey', methods=['GET', 'POST'])
def take_survey():
    current_question = int(request.args.get('question',0))
    if request.method == 'POST':
        response = request.form.get('response')
        if response:
            session['responses'] = session.get('responses', {})
            session['responses'][current_question] = response
            current_question += 1
            if current_question == len(survey.questions):
                return render_template('responses.html', responses = session['responses'])
            else:
                return redirect(url_for('take_survey', question = current_question))
        else:
            flash('Please answer the question before moving to the next')
            return redirect(url_for('take_survey', question = current_question))
    else:
        return render_template('survey.html', question = survey.questions[current_question], current_question = current_question)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import uuid
from setup_config import insert_questions_into_json_cfg

app = Flask(__name__,template_folder='./')

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        question1 = request.form.get('question1')
        question2 = request.form.get('question2')
        responses = [question1, question2]
        user_id = uuid.uuid1()
        # For demonstration, print to console
        #print(responses, user_id)
        user_cfg = insert_questions_into_json_cfg(responses, user_id)

        return redirect(url_for('thank_you'))

    return render_template('survey.html')


@app.route('/thank-you')
def thank_you():
    return "<h2>Thank you for submitting the survey!</h2>"


if __name__ == '__main__':
    app.run(debug=True)
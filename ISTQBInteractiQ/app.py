from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import openpyxl
import time
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to your secret key
data_source_directory = 'data_source'
app.config['SESSION_TYPE'] = 'filesystem'  # You can change it to 'redis' or any other session type
Session(app)


def read_data_source():
    """Read the directory and return a list of xlsx files."""
    try:
        return [filename for filename in os.listdir(data_source_directory) if filename.endswith('.xlsx')]
    except Exception as e:
        flash(f"Error reading data source: {str(e)}")  # Handle error
        return []


def read_survey(filename):
    """Read the survey questions from the specified Excel file."""
    try:
        workbook = openpyxl.load_workbook(os.path.join(data_source_directory, filename))
        sheet = workbook.active
        questions = []

        # Read each question
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip header
            if row:  # Ensure the row is not empty
                question_data = {
                    "id": row[0],
                    "question": row[1],
                    "correct_answer": row[2],
                    "title": row[3],
                    "options": {"A": row[4], "B": row[5], "C": row[6], "D": row[7]}
                }
                questions.append(question_data)

        return questions
    except Exception as e:
        flash(f"Error reading survey file '{filename}': {str(e)}")
        return []


@app.route('/')
def survey_list():
    """Display the list of available surveys."""
    surveys = read_data_source()
    return render_template('surveys.html', surveys=surveys)


@app.route('/survey/<filename>', methods=['GET'])
def start_survey(filename):
    """Initialize the survey and redirect to the first question."""
    questions = read_survey(filename)
    if not questions:  # Check if questions are empty
        flash("No questions found in the selected survey.")
        return redirect(url_for('survey_list'))

    session['questions'] = questions
    session['current_question'] = 0
    session['correct_answers'] = 0
    session['start_time'] = time.time()
    return redirect(url_for('question'))


@app.route('/question', methods=['GET', 'POST'])
def question():
    """Display the current question and handle user submissions."""
    if 'current_question' not in session:
        flash("No survey selected. Please select the survey from the list.")
        return redirect(url_for('survey_list'))

    # Load questions again as needed
    questions = session.get('questions')
    current_question_index = session['current_question']

    # Checking if current question index is valid
    if current_question_index >= len(questions):
        return redirect(url_for('final_result'))

    if request.method == 'POST':
        user_answer = request.form.get('option', None)
        if not user_answer:
            flash("No answer selected. Please select an answer.")
            return redirect(url_for('question'))

        correct_answer = questions[current_question_index]['correct_answer']
        session['user_answer'] = user_answer

        # Compare the user answer with the correct answer
        if user_answer == correct_answer:
            session['correct_answers'] += 1

        session['current_question'] += 1
        return redirect(url_for('result_question'))

    question_data = questions[current_question_index]
    preformatted_title = question_data['title']
    formatted_title = preformatted_title.replace("\n", '<br>')
    questions[current_question_index]['title'] = formatted_title
    return render_template('question.html', question=question_data, question_number=current_question_index + 1)


@app.route('/result_question', methods=['GET'])
def result_question():
    """Display the result of the last question including user's answer."""
    if 'user_answer' not in session:
        flash("No user answer found. Please select an answer first.")
        return redirect(url_for('question'))

    current_question_index = session['current_question'] - 1
    questions = session['questions']
    question_data = questions[current_question_index]

    # Retrieve the user's answer from the session
    user_answer = session['user_answer']
    correct_answer = question_data['correct_answer']

    return render_template(
        'result_question.html',
        question=question_data,
        user_answer=user_answer,
        correct_answer=correct_answer,
        question_number=current_question_index + 1
    )


@app.route('/final_result')
def final_result():
    """Display the final results of the survey."""
    correct_count = session['correct_answers']
    total_questions = len(session['questions'])
    time_spent = time.time() - session['start_time']
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0

    # Clear session data after final result page
    session.clear()

    return render_template(
        'final_result.html',
        correct_count=correct_count,
        total=total_questions,
        percentage=round(percentage),
        time_spent=round(int(time_spent)/60)
    )


# Error handler
@app.errorhandler(Exception)
def handle_error(e):
    """Catch and handle errors in the app."""
    flash(f"An unexpected error occurred: {str(e)}")
    return redirect(url_for('survey_list'))


if __name__ == '__main__':
    app.run(debug=True)

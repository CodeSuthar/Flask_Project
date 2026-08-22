from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():

    date1 = request.form['date1']
    date2 = request.form['date2']

    first_date = datetime.strptime(date1, '%Y-%m-%d')
    second_date = datetime.strptime(date2, '%Y-%m-%d')

    difference = abs((second_date - first_date).days)

    return render_template(
        'index.html',
        date1=date1,
        date2=date2,
        difference=difference,
        message='Date difference calculated successfully!'
    )


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    units = int(request.form['units'])

    bill = units * 5

    if bill <= 100:
        message = f"Your electricity bill is ${bill}. You are within the budget."
    elif bill <= 200:
        message = f"Your electricity bill is ${bill}. You are slightly over the budget."
    else:
        message = f"Your electricity bill is ${bill}. You are significantly over the budget."

    object = {
        'units': units,
        'bill': bill,
        'message': message
    }
    return render_template('index.html', result=object)

if __name__ == '__main__':
    app.run(debug=True)
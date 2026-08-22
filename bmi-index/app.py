from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():

    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])

    bmi = weight / (height * height)
    bmi = round(bmi, 2)

    if bmi < 18.5:
        status = "Below the standard adult BMI range"
        message = "Your BMI has been calculated successfully."
    elif bmi < 25:
        status = "Within the standard adult BMI range"
        message = "Your BMI has been calculated successfully."
    elif bmi < 30:
        status = "Above the standard adult BMI range"
        message = "Your BMI has been calculated successfully."
    else:
        status = "High BMI range"
        message = "Your BMI has been calculated successfully."

    return render_template(
        'index.html',
        name=name,
        weight=weight,
        height=height,
        bmi=bmi,
        status=status,
        message=message
    )


if __name__ == '__main__':
    app.run(debug=True)
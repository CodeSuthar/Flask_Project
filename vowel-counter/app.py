from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/count', methods=['POST'])
def count_vowels():

    text = request.form['text']

    vowels = "aeiouAEIOU"

    count = sum(1 for char in text if char in vowels)

    return render_template(
        'index.html',
        text=text,
        count=count,
        message="Vowels counted successfully!"
    )


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/to_back', methods=['POST'])
def to_back():
    print("True")
    return "Bob"

if __name__ == '__main__':
    app.run(debug=True)
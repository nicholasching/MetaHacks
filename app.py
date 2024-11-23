from flask import Flask, render_template, request
import os
from audioTranscriber import audioTranscriber as at
from summaryGenerator import summaryGenerator as sg

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/to_back/<test>', methods=['POST'])
def to_back(test):
    file = open("text.txt", "w")
    file.write(at.transcribeAudio("sampleAudio.wav"))
    return sg.generateSummary("text.txt")

if __name__ == '__main__':
    app.run(debug=True)
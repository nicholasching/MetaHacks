from flask import Flask, render_template, request
import os
from audioTranscriber import audioTranscriber as at
from summaryGenerator import summaryGenerator as sg
from flashcardGenerator import flashcardGenerator as fg

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/to_back/<test>', methods=['POST'])
def to_back(test):
    file = open("text.txt", "w")
    file.write(at.transcribeAudio("sampleAudio.wav"))
    file.close()
    return sg.generateSummary("text.txt")

@app.route('/to_back/gen_cards', methods=['GET'])
def generate_cards(path):
    with open("text.txt", "r") as file:
        line = file.readline() 
        fg.generateCards(line)
        return fg.getCards()
        

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
import os
from audioTranscriber import audioTranscriber as at
from summaryGenerator import summaryGenerator as sg
from flashcardGenerator import flashcardGenerator as fg

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/to_back/<path>', methods=['POST'])
def to_back(path):
    # Get the audio file from the request
    audio_file = request.files['audio']
    if audio_file:
        # Save the audio file
        if not os.path.exists(f"uploads/{path}"):
            os.mkdir(f"uploads/{path}")
        audio_file.save(f"uploads/{path}/recording.wav")
    
    file = open(f"uploads/{path}/transcript.txt", "w")
    file.write(at.transcribeAudio(f"uploads/{path}/recording.wav"))
    file.close()
    
    return sg.generateSummary(f"uploads/{path}/transcript.txt")

@app.route('/to_back/gen_cards', methods=['GET'])
def generate_cards(path):
    with open("text.txt", "r") as file:
        line = file.readline() 
        fg.generateCards(line)
        return fg.getCards()
        

if __name__ == '__main__':
    app.run(debug=True)
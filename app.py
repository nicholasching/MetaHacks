from flask import Flask, render_template, request
import os
from audioTranscriber import audioTranscriber as at
from summaryGenerator import summaryGenerator as sg
from flashcardGenerator import flashcardGenerator as fg
import json

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
    
    file = open(f"uploads/{path}/summary.txt", "w")
    output = sg.generateSummary(f"uploads/{path}/transcript.txt")
    file.write(output)
    file.close()

    return output

@app.route('/get_summary/<path>', methods=['POST'])
def get_summary(path):
    if os.path.exists(f"uploads/{path}/summary.txt"):
        file = open(f"uploads/{path}/summary.txt")
        returnString = file.readline()
        file.close()
        return returnString
    else: 
        return "false"

@app.route('/gen_cards/<path>', methods=['POST'])
def gen_cards(path):
    if os.path.exists(f"uploads/{path}/transcript.txt"):
        with open(f"uploads/{path}/flashcards.JSON", "w") as jsonFile:
            print("transcript?")
            with open(f"uploads/{path}/transcript.txt", "r") as file:
                line = file.readline()
                if line:
                    gen = fg(line)
                    gen.generateCards(line)
                    json.dump(gen.getCards(), jsonFile)
                    print(type(gen.getCards))
                    return gen.getCards()
                else: 
                    print("no transcript")
                    return "false" 
    else: 
        print("no transcript")
        return "false" 
        
@app.route('/get_cards/<path>', methods=['POST'])
def get_cards(path):
    jsonString = None
    if os.path.exists(f"uploads/{path}/flashcards.JSON"):
        with open(f"uploads/{path}/flashcards.JSON", "r") as jsonFile:
            if jsonFile.readline() != '':
                jsonFile.seek(0)
                print(jsonFile.readline())
                jsonFile.seek(0)
                jsonString = json.load(jsonFile)
                return json.dumps(jsonString)

    return "false" 

if __name__ == '__main__':
    app.run(debug=True)
import speech_recognition as sr
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

class audioTranscriber:
    
    def transcribeOneAudio(path):
        # create a speech recognition object
        r = sr.Recognizer()
        # use the audio file as the audio source
        with sr.AudioFile(path) as source:
            audio_listened = r.record(source)
            # try converting it to text
            text = r.recognize_google(audio_listened)
        return text 
  
    def transcribeAudio(path, minutes=3):
        """Splitting the large audio file into fixed interval chunks
        and apply speech recognition on each of these chunks"""
        
        # open the audio file using pydub
        sound = AudioSegment.from_file(path)  
        # split the audio file into chunks
        chunk_length_ms = int(1000 * 60 * minutes) # convert to milliseconds
        chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]
        folder_name = "audio-fixed-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            try:
                text = audioTranscriber.transcribeOneAudio(chunk_filename)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
        # return the text for all chunks detected
        return whole_text
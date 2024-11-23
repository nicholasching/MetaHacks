from ollama import chat
from ollama import ChatResponse
from audioTranscriber import audioTranscriber as at

text = at.get_large_audio_transcription_fixed_interval("sampleAudio.wav")
file = open("text.txt", "w")
file.write(text)
print("Trascription Complete: ")

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': f"The text provided after the semicolons are an audio transcription from a lecture, summarize the content: {text}",
  },
])

print(response.message.content)
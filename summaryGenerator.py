from ollama import chat
from ollama import ChatResponse

class summaryGenerator:
    
  def generateSummary(path):
    file = open(path)
    text = file.readline()
    file.close()

    response: ChatResponse = chat(model='llama3.2', messages=[
      {
        'role': 'user',
        'content': f"The text provided after the semicolons are an audio transcription from a lecture, summarize the content: {text}",
      },
    ])

    return response.message.content
from ollama import chat
from ollama import ChatResponse

class summaryGenerator:
    
  def generateSummary(path):
    file = open(path)
    text = f"summarize this lecture audio: {file.readline()}"
    file.close()
    response: ChatResponse = chat(model='llama3.2', messages=[
      {
        'role': 'user',
        'content': text,
      },
    ])

    return response.message.content
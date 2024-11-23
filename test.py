
"""from ollama import chat

stream = chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'tell me 3 jokes formatted with the a question and answer at different indices'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)"""


from ollama import chat
from ollama import ChatResponse
import json

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'In the following format, give me 3 Questions and Answers about: Question,Answer',
  },
])

print(response.message.content)
from ollama import chat
from ollama import ChatResponse
import json

class flashcardGenerator() :
  def __init__(self, text):
    self.transcription = text.replace('\'', '')
    self.cards = None

  def generateCards(self):
    flashcardString: ChatResponse = chat(model='llama3.2', messages=[
      {
        'role': 'user',
        'content': "based on the text: " + self.transcription + ', generate exactly 1 calculation based question and its corresponding answer. Return the result in the form of a JSON object with the following structure and without any extra space or text: \n'
        + '{\n'
        + '\t\"card1\": {\n'
        + '\t\t\"q\": \"Question text here\",\n'
        + '\t\t\"a\": \"Answer text here\"\n'
        + '\t}\n'
        + '}'
      },
    ])
    msg = flashcardString.message.content
    ind = msg.index('{') 
    print(msg[ind:])
    self.cards = json.loads(msg[ind:])
    print(self.cards)
    
  def getCards(self): 
    if self.cards == None: raise Exception ("No cards were generated")
    else: return self.cards

def main():
  gen = flashcardGenerator('Cats are cool')
  gen.generateCards()
  cardsJSON = gen.getCards()
  print(type(cardsJSON))
  print(cardsJSON["card1"])

main()
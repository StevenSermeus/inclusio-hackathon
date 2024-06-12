import json
from .database import get_gpt_response, get_gpt_image_response
import re           
class Sentence:
    def __init__(self, content:str, coeff:float, img_path:str) -> None:
        self.content = content
        self.coeff = coeff
        self.img_path = img_path
        
    def simplify(self):
        self.content = get_gpt_response(self.content)
    
    def get_coeff(self, words_occurences:dict[str:float]):
        content_without_ponct = re.sub(r'[:;,&|#@"(§!{})_~;.<>€$£?«»{0-9}]', '', self.content)
        print(content_without_ponct)
        for word in content_without_ponct.split(' '):
            word = word.lower()
            
            if word in ["le", "la", "les", "un", "une", "des", "du", "de", "d'"]:
                self.coeff += 0.9
            elif word in ["et", "ou", "donc", "or", "ni", "car"]:
                self.coeff += 0.4
            elif word in ["je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles", "papa", "maman", "princesse", "or", "plein", "jolie", "chevalier", "marier", "mariée", "fois"]:
                self.coeff += 0.9
            elif word in words_occurences:
                self.coeff += words_occurences[word]
            else:
                self.coeff += 0.5
        self.coeff /= len(content_without_ponct.split(' '))
        self.coeff = (1-self.coeff)*100
                
    
    def get_image(self):
        self.img_path = get_gpt_image_response(self.content)
        
    
    def to_json(self):
        return json.dumps(self.__dict__)
    
    @classmethod
    def from_json(cls, text):
        data = json.loads(text)
        content = data['content']
        coeff = data['coeff']
        img_path = data['img_path']
        return cls(id, content, coeff, img_path)
from openai import OpenAI
import requests
import os
import uuid
import pandas as pd
def get_words_occurences(path:str='ressources/ranking.csv')->dict[str:float]:
    # Get the list of words from the database with their complexity
    data = pd.read_csv(path)
    words_occurences = data.set_index('word').to_dict()['ranking']
    return words_occurences


def get_gpt_response(sentence:str)->str:
    prompt = """L'éducation inclusive doit respecter 4 principes. 1. L'accessibilité : en veillant à ce que les installations, le matériel pédagogique, les outils technologiques et les ressources soient accessibles à tous les élèves, indépendamment de leurs limitations.
2. L'adaptation et la flexibilité : en adoptant une approche flexible de l’enseignement et mettre en place des pratiques pédagogiques qui s'adaptent aux différents styles d'apprentissage, capacités et besoins des élèves. Il s’agit par exemple des classes flexibles, des classes autonomes, des aménagements spécifiques, de la différenciation… 3 La diversité : en utilisant et en proposant des ressources pédagogiques variées, allant des manuels et des outils scolaires dits « traditionnels » aux supports et outils numériques, ceci afin de s'assurer que chaque élève puisse avoir accès à un enseignement pertinent pour le développement de son propre potentiel.
4. L'engagement et la collaboration : en encourageant l’implication de l’ensemble des acteurs (enseignants, direction, élèves, parents, accompagnateurs sociaux et paramédicaux) et leur collaboration, notamment pour comprendre les besoins individuels des élèves et soutenir ensemble et de manière cohérente leur apprentissage.
En tant qu'enseignant pour enfants de 6 à 12 ans, préoccupé par l'éducation inclusive, tu dois t'exprimer en phrase simple, avec un vocabulaire élémentaire. Je vais donc te donner des phrases complexes, et tu dois les simplifier au maximum, avec un nombre minimum de mots, pour qu'elles soient compréhensibles pour les enfants. Simplifie-moi la phrase suivante: 
"""
    client_ai = OpenAI(
        api_key='sk-...', # Replace with our API key
    )
    response =  client_ai.chat.completions.create(
        
        messages=[
            {
                "role": "user",
                "content": prompt+sentence,
            }
        ],
        model="gpt-4",
    )
    return response.choices[0].message.content
    
    

def get_gpt_image_response(sentence:str):
    name = str(uuid.uuid4())+'.png'

    directory = './static'

    prompt = """
En tant qu'enseignant pour enfants de 6 à 12 ans, préoccupé par l'éducation inclusive, tu dois proposer des images qui illustrent des phrases simples. N'utilise surtout pas de texte dans l'image. Tu dois générer une image claire, simple et compréhensible sous la forme d'un pictogramme, pour que des enfants de 6 à 12 ans puissent comprendre la phrase suivante:
"""


    client_ai = OpenAI(
        api_key='sk-...', # Replace with our API key
    )

    response = client_ai.images.generate(
    model="dall-e-3",
    prompt=prompt+sentence,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    filename = os.path.join(directory, name)  # Modifier l'extension selon le format de l'image
    #create the file on the good directory




    url = response.data[0].url

    res = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(res.content)

    return name
    

# chatgpt exemple
# if __name__ == '__main__':
    
#     sentence = "En géométrie euclidienne, un triangle équilatéral est un triangle dont les trois côtés ont la même longueur. Ses trois angles internes ont alors la même mesure de 60 degrés, et il constitue ainsi un polygone régulier à trois sommets."

#     print(get_gpt_response(sentence)) # Should print a response from GPT-3.5

#     sentence = "Dans les formes, un triangle équilatéral est un triangle avec trois côtés qui sont tous de la même taille. Ses trois coins ont la même taille de 60 degrés. C'est une forme régulière avec trois pointes."
    
#     get_gpt_image_response(sentence) # Should print a response from DALL-E-3
    
    




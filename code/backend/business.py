from .database import get_words_occurences

def get_word_occurence_dict(path:str='ressources/ranking.csv')->dict[str:float]:
    return get_words_occurences(path)
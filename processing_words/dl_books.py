import requests
import os
from time import sleep

files = os.listdir('../ressources/books_numbers')

for file in files :
    number = file[:len(file)-5]
    filename = f"{number}.pdf"
    url = f"https://litterature-jeunesse-libre.fr/bbs/download/{number}/pdf/{filename}"
    path = f"../ressources/files_words/{filename}"

    print(f"Downloading {filename} from {url}")

    response = requests.get(url, stream = True)
    with open(path,"wb") as pdf:
        for chunk in response.iter_content(chunk_size=1024):
            # writing one chunk at a time to a pdf file
            if chunk:
                pdf.write(chunk)
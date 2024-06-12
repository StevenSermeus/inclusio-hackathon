# Requires installing thoses packages: pdfplumber, pandas, numpy, docxpy
# pip install pdfplumber pandas numpy docxpy
# This script is used to count the number of words in a pdf or docx file and save the result in a csv file

import pdfplumber as pdf 
import pandas as pd 
import numpy as np 
import docxpy
import re
import os


if __name__=='__main__':
    dico_word = {}
    txt = ""
    exclusion_list = ['', 'au','aux', 'rien', 'de', 'la', 'le', 'les', 'un', 'une', 'des', 'du', 'ce', 'cette', 'ces', 'cet', 'avec', 'c', 'd', 'l', 'm', 'n', 's', 't', 'y', 'j', 'q', 'v', 'x', 'z', 'a', 'b', 'e', 'f', 'g', 'h', 'i', 'o', 'p', 'r', 'u', 'w', 'k', 'à', 'â', 'ç', 'è', 'é', 'ê', 'î', 'ï', 'ô', 'û', 'ü', 'œ', 'ë', 'ù', 'ä', 'ö', 'ß', 'á', 'í', 'ó', 'ú', 'ý', 'ã', 'õ', 'ñ']

    files = os.listdir('../ressources/files_words')
    print(f"Files found : {files}")
    total = len(files)
    processed = 0
    for file in files :
        print(f"Processing file {file}")
        if file.endswith('.pdf'):
            print(file)
            try:
                with pdf.open(f'../ressources/files_words/{file}') as pdf_file:
                    for page in pdf_file.pages:
                        txt += page.extract_text()
            except:
                print(f"Error while processing {file}")
                continue
        elif file.endswith('.docx'):
            print(file)
            try:
                txt = docxpy.process(f'../ressources/files_words/{file}')
            except:
                print(f"Error while processing {file}")
                continue
        txt_sub_apo = re.sub(r'[\'’-]', ' ', txt)
        txt_mod = re.sub(r'[:;,&|#@"(§!{})_/*+=~;.<>€$£?«»{0-9}]', '', txt_sub_apo)
        txt_mod = txt_mod.lower()
        tb_test = txt_mod.split(' ')
        for word in tb_test:
            if word.__contains__('\n') or word.__contains__('\\') or word in exclusion_list or len(word) < 4 :
                continue
            else :
                if word not in dico_word:
                    dico_word[word] = 1
                else:
                    dico_word[word] += 1
        processed += 1
        print(f"Processed {processed} files out of {total}")
    df = pd.DataFrame(dico_word.items(), columns=['word', 'count'])
    df = df.sort_values(by='count', ascending=False)
    print("Done processing files")
    df.to_csv('../ressources/words_count.csv', index=False)


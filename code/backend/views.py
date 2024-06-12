from flask import Flask, request,jsonify,render_template,send_file,send_from_directory
from .model import Sentence
from flask_cors import CORS, cross_origin
import json
from .business import get_word_occurence_dict
import random
app = Flask(__name__,static_folder='/hackaton-cslab/static')
CORS(app, origins="*")

#app.config.from_object('config')
global words_occurences 
words_occurences = get_word_occurence_dict()

## Get the list of sentences from the frontend
@app.route('/check', methods=['POST', 'GET'])
@cross_origin(origins="*")
def get_check():
    if request.method == 'POST': # We receive a list of sentences
        # Get the list of sentences from the frontend
        sentences = request.get_json()
        sentences_2 = sentences.get('sentences', [])
        response = []
        for sentence in sentences_2:
            s = Sentence(sentence, 0, "")
            s.get_coeff(words_occurences)
            print(s.coeff)
            response.append({
                "sentence": s.content,
                "coeff":  s.coeff,
            })
            
        return json.dumps(response)
       


@app.route('/simplify', methods=['POST', 'GET'])
@cross_origin(origins="*")     
def get_simplify():
    if request.method == 'POST':
        sentence = request.get_json()
        #print(sentence)
        s = Sentence(sentence["phrase"], 0, "")
        print(s.content)
        s.simplify()
        s.get_coeff(words_occurences)
        print("GPTT" + s.content)
        return json.dumps({'phrase':s.content, 'coeff':s.coeff})
        


@app.route('/get_image', methods=['POST', 'GET'])
def get_image():
    if request.method == 'POST':
        # Get the list of sentences from the frontend
        sentences = request.get_json()
            # Create a Sentence Object
        s = Sentence(sentences["phrase"], 0, "")
            #### PUT IN BUSINESS LOGIC ####
            # Ask the Sentence Object to get an image
        s.get_image()
        
        return json.dumps({"url": s.img_path})

@app.route('/static/<string:filename>', methods=['GET'])
def get_static_image(filename):
    print(filename)
    return send_file('../../static/' + filename )
    


@app.route('/image')
def get_staticss_image():
    return send_file('../../static/a25e9334-2dc0-454f-83c0-03c6908363b7.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
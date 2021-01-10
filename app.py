
# importing libraries 
from flask import Flask, jsonify, request
from word_in_audio import WordInAudio
    


app = Flask(__name__)


@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        path = request.form.get('path')
        word_search = request.form.get('word_search')
        language = request.form.get('language')

    obj = WordInAudio(path, word_search, language)
    get_times = obj.get_large_audio_transcription()
    return jsonify(get_times)


if __name__=='__main__':
    app.run(debug=True)
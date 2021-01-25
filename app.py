
# importing libraries 
from flask import Flask, jsonify, request
from word_in_audio import WordInAudio
import time
import redis
from rq import Queue
    


app = Flask(__name__)

r = redis.Redis()
q = Queue(connection=r)

def background_task(n):

    with app.app_context():
        path = n[0]
        word_search = n[1]
        language = n[2]


        print("Task is running")

        obj = WordInAudio(path, word_search, language)
        get_times = obj.get_large_audio_transcription()


        print("Task complete")

        print(get_times)

        return (jsonify(get_times))


@app.route('/', methods = ["GET", "POST"])
def home():

    my_list = []
    
    if request.method == "POST":

        path = request.form.get('path')
        word_search = request.form.get('word_search')
        language = request.form.get('language')

        my_list.extend((path, word_search, language))

        job = q.enqueue(background_task, my_list )

        # q_len = len(q)
        return f"Task ({job.id}) added to queue at {job.enqueued_at}"

    return "No value for count provided"


if __name__=='__main__':
    app.run(debug=True)
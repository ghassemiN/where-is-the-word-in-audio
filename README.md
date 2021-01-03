## Where is the word in audio 

It was interesting for me to know if it is possible to find out without listening to the audio file, whether the word we want is included in the audio or not! I did a search and found out how an audio file is converted to text. Then all I did was add the search section and calculate the approximate time.
So all you need is a wav file, and a word to looking for.

## Requrments:
before run the script in terminal, be sure that you've already installed python3 and ffmpeg.

###If you have not installed ffmpeg on your machine already: `apt update && apt install -y ffmpeg`

Install requirements: `pip3 install -r requirements.txt`


## Run the script
open find_word_audio.py and edit these lines then save it:
`path = "Your-Audio_file.wav"`
`word_search = "You_word_to_search"`
then run it: `python3 find_word_audio.py`



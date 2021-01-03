# importing libraries 
import wave
import sys
import contextlib
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from os import path
from pydub import AudioSegment
import math
import datetime

# create a speech recognition object
r = sr.Recognizer()

# The audio file
path = sys.argv[1]

# The word to looking for in the audio file
word_search = sys.argv[2]

# The language of audio file, it could be english (en-US), Farsi(fa-IR), Turkish(tr-TR) and ...
language = sys.argv[3]

# create and open a file to write
text_audio = open("text_speech.txt", "a")

# create a list to store chunks name
chunks_name_list = []

# create a list to store chunk's duration
chunks_duration_list = []

# a function that checks a wav file duration
def get_wav_duration(path):
	with contextlib.closing(wave.open(path,'r')) as f:
	    frames = f.getnframes()
	    rate = f.getframerate()
	    duration = frames / float(rate)
	return(duration)

# a function that gives an estimated time (begin and end) for the word in a wav file
# It needs the chunks name and duration lists and the chunk file that involves the word
def word_estimated_time(chunks_name_list, chunks_duration_list, chunk_include_word):
	# The begin and end times indicate the range in which you will find the word
	begin_time = 0
	index = chunks_name_list.index(chunk_include_word)
	for i in range(0, index):
		# calculate the begin time of the chunk file involved the word
		begin_time =  begin_time + chunks_duration_list[i]	
	#calculate the end time of the chunk file involved the word
	end_time = begin_time + chunks_duration_list[index]
	# round begin and end time
	begin_time = math.floor(begin_time)
	end_time = math.ceil(end_time)
	begin_time = str(datetime.timedelta(seconds=begin_time))
	end_time = str(datetime.timedelta(seconds=end_time))

	return begin_time, end_time
	

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    chunks_folder_path = "/tmp/audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(chunks_folder_path):
        os.mkdir(chunks_folder_path)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `chunks_folder_path` directory.
        chunk_filename = os.path.join(chunks_folder_path, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # insert file name and it's duration to lists
        chunks_name_list.insert(i,f"chunk{i}.wav")
        chunks_duration_list.insert(i,get_wav_duration(chunk_filename))
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened , language=language)
                # find a word in the texe
                find_word = text.find(word_search)
                # checks if this chunk's text include the word, then estimate time
                if find_word != -1 :
                	chunk_include_word = f"chunk{i}.wav"
                	begin_time , end_time = word_estimated_time(chunks_name_list, chunks_duration_list, chunk_include_word)
                	print ("The word you are searching for is between: ", begin_time, " and ", end_time )
                	
     			# write the text in the file
                text_audio.write(text)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                # uncomment it if you want to see the text of every chunks in terminal
                # print(chunk_filename, ":", text)
                whole_text += text

    
    # close the file 
    text_audio.close()

    # return the text for all chunks detected and estimated time that includes the word you are searching for
    return whole_text



print ("Start to convert audio to text and search your word in it, be patient :)")
get_large_audio_transcription(path)
print ("The end")
# uncomment it if you want to see the whole text of wav file in terminal
# print("\nFull text:", get_large_audio_transcription(path))
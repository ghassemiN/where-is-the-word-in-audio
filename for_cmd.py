from word_in_audio import WordInAudio
import sys

try:
    # The audio file
    path = sys.argv[1]
    # The word to looking for in the audio file
    word_search = sys.argv[2]
    word_search = word_search.lower()
    # The language of audio file, it could be english (en-US), Farsi(fa-IR), Turkish(tr-TR) and ...
    language = sys.argv[3]
except:
    print ("Please enter the arguments: path of the audio file, the word you want search and language of audio")
    sys.exit()

# create an obj from class
obj = WordInAudio(path, word_search, language)


print ("Start to convert audio to text and search your word in it, be patient :)")
print(obj.get_large_audio_transcription())
print ("The end")
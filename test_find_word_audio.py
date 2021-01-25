import unittest
import contextlib
import wave



path = "test.wav"

class TestStringMethods(unittest.TestCase):


	def test1_get_wav_duration(self):
		with contextlib.closing(wave.open(path,'r')) as f:
		    frames = f.getnframes()
		    rate = f.getframerate()
		    duration = frames / float(rate)
		    duration = round(duration, 3)
		self.assertEqual(duration, 06.354)



if __name__ == '__main__':
    unittest.main()
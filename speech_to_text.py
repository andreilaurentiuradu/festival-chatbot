# import required libraries
import openai
# import required libraries
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

# Sampling frequency
freq = 44100

# Recording duration
duration = 5

# Start recorder with the given values
# of duration and sample frequency
recording = sd.rec(int(duration * freq),
				samplerate=freq, channels=2)

# Record audio for the given number of seconds
sd.wait()

# This will convert the NumPy array to an audio
# file with the given sampling frequency
write("recording0.wav", freq, recording)


openai.api_key = "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"
audio_file = open("recording0.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)
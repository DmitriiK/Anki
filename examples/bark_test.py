from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
     But I also have other interests such as playing tic tac toe.
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
  
# play text in notebook
# Audio(audio_array, rate=SAMPLE_RATE)
print("converted")
import numpy as np
int_audio_arr = (audio_array * np.iinfo(np.int16).max).astype(np.int16)

# save as wav
from scipy.io import wavfile
wavfile.write("my_bark_sfile.file.wav", SAMPLE_RATE, int_audio_arr)

# save as mp3
from pydub import AudioSegment
audio_segment = AudioSegment(
    int_audio_arr.tobytes(),
    frame_rate=SAMPLE_RATE,
    sample_width=int_audio_arr.dtype.itemsize,
    channels=1,
)
audio_segment.export("my_bark_file.mp3", format="mp3");
print("done")
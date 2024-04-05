import os
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings, play, save
from elevenlabs.client import ElevenLabs

from dotenv import load_dotenv

load_dotenv()
client = ElevenLabs( api_key=os.getenv('ELEVEN_LABS_API_KEY'))
def generate_audio(text: str, file_name: str = '', directory_name = ''):
  voice= 'Sarah' # "Ahmet Çiçek"
  file_name = file_name or voice
  if directory_name:
    file_name = os.path.join(directory_name, file_name)
  audio = client.generate(
  text=text,
  voice=voice,
  model="eleven_multilingual_v2"
  ,
)
  save(audio=audio, filename=f'{file_name}.mp3')

def test():
# text = "Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!"
  text = "Ben----bunu bilmiyordum.----Hava çok sıcak oldu."
  generate_audio(text, 'test_turkish')
  
if __name__ =="__main__":  
  test()
  



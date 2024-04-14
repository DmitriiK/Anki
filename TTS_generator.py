
import os

from elevenlabs.client import ElevenLabs
from elevenlabs import save  # Voice, VoiceSettings, play,

import config_data as cfg


class TTS_GEN:
    def __init__(self, voice: str = 'Sarah', model: str = 'eleven_multilingual_v2'):
        self.client = ElevenLabs(api_key=cfg.ELEVEN_LABS_API_KEY)
        self.voice = voice
        self.model = model

    def generate_audio(self, tts: str, file_name: str = '', directory_name: str = ''):
        file_name = file_name or self.voice
        if directory_name:
            file_name = os.path.join(directory_name, file_name)
        audio = self.client.generate(text=tts, voice=self.voice, model=self.model,)
        save(audio=audio, filename=f'{file_name}.mp3')


def test():
    #  text = "Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!"
    text = "Ben----bunu bilmiyordum.----Hava çok sıcak oldu."
    tts = TTS_GEN()
    tts.generate_audio(text, 'test_turkish')


if __name__ == "__main__":
    test()


import os
from typing import Iterable, Tuple, List
import logging

from elevenlabs.client import ElevenLabs
from elevenlabs import save  # Voice, VoiceSettings, play,
from elevenlabs import play  # to use play need to ffmpeg to be installed 
import config_data as cfg

if cfg.FFMPEG_PATH:
    os.environ['PATH'] += os.pathsep + cfg.FFMPEG_PATH  # for audio player


class TTS_GEN:
    def __init__(self, voice: str = 'Sarah', model: str = 'eleven_multilingual_v2', our_dir_path=''):
        self.client = ElevenLabs(api_key=cfg.ELEVEN_LABS_API_KEY)
        self.voice = voice
        self.model = model
        self.our_dir_path = our_dir_path
     
    @staticmethod
    def text_transform(tts: str) -> str:
        """To make model separate words more distinctly.
        Args:
            tts (str): _description_

        Returns:
            str: _description_
        """
        silence = ' ---- '
        return tts.replace(r'\n', silence + r'\n')  # .replace(' ', silence)

    def generate_audio(self, tts: str, file_name: str = '',  play_sound=False):
        file_name = file_name or self.voice
        file_name = file_name + '.mp3'
        if self.our_dir_path:
            file_name = os.path.join(self.our_dir_path, file_name)
        if os.path.exists(file_name):
            logging.warning(f'file {file_name} exists. skipping')
            return
        logging.info(f'producing audio for text having len {len(tts)} chars')
        audio = self.client.generate(text=tts, voice=self.voice, model=self.model,)
        if play_sound:
            print(tts)
            play(audio)
        else:
            save(audio=audio, filename=file_name)
            logging.info(f'wrote audio to file {file_name}.')

    def generate_audio_batch(self, items: Iterable[Tuple[str, List[str]]], play_sound=False):
        """generate audio files in batch mode
        Args:
            items (Iterable[Tuple[str, List[str]]]):words and examples of usages
            play_sound (bool, optional): If yes, play sound before writhing to file. Defaults to False.
        """
        cnt_len = 0
        for word, exs in items:
            ex_str = r'.\n'.join(exs)
            ex_str = self.text_transform(ex_str)
            cnt_len += len(ex_str)
            self.generate_audio(tts=ex_str, file_name=word, play_sound=play_sound)
            print(f'{cnt_len=}')


def test():
    #  text = "Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!"
    text = "Ben----bunu bilmiyordum.----Hava çok sıcak oldu."
    tts = TTS_GEN()
    tts.generate_audio(text, 'test_turkish')


if __name__ == "__main__":
    test()

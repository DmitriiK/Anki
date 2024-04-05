# %%
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
from TTS.api import TTS

xx = TTS().list_models()
##print(xx.models_dict)
# https://colab.research.google.com/drive/1F_gatrMCSDwtlXuQHCGSA_p096q1YiNI?usp=sharing#scrollTo=i8_ug-STJhn_
# here should be the path to where pip(or conda or whatever) put TTS packages
path = "/home/dklmn/projects/Anki/.venv/lib/python3.10/site-packages/TTS/.models.json"

model_manager = ModelManager(path)
model_name  = "tts_models/en/ljspeech/tacotron2-DDC" # "tts_models/de/thorsten/tacotron2-DDC"
model_name  = "tts_models/tr/common-voice/glow-tts"



text = "Hava çok sıcak oldu."
# Note: for some reason id does not work with upper case letters, getting "[!] Character 'H' not found in the vocabulary. Discarding it."
# tts = TTS(model_name=model_name, progress_bar=True, gpu=False)
# Run TTS
# tts.tts_to_file(text=text, file_path="output_test.wav")


# %% 
model_path, config_path, model_item = model_manager.download_model(model_name)
vocoder_model = model_item["default_vocoder"]
voc_path, voc_config_path, _ = model_manager.download_model(vocoder_model)

syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)



outputs = syn.tts(text, language_name='tr')
syn.save_wav(outputs, "TTS-1.wav")
print('done')
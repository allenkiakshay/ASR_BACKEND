import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"
import sys
sys.path.append("/home/development/akshayb/shyam_webservice/Text2SpeechApp/TTS/ForwardTacotron/")

import numpy as np
import torch

from TTS.ForwardTacotron.models.forward_tacotron import ForwardTacotron

from TTS.ForwardTacotron.utils.marathi.cleaners import MarathiCleaner
from TTS.ForwardTacotron.utils.marathi.tokenizer import MarathiTokenizer

from TTS.ForwardTacotron.utils.hindi.cleaners import HindiCleaner
from TTS.ForwardTacotron.utils.hindi.tokenizer import HindiTokenizer

#from TTS.ForwardTacotron.utils.bengali.cleaners import BengaliCleaner
#from TTS.ForwardTacotron.utils.bengali.tokenizer import BengaliTokenizer

from TTS.ForwardTacotron.utils.gujarati.cleaners import GujaratiCleaner
from TTS.ForwardTacotron.utils.gujarati.tokenizer import GujaratiTokenizer

from TTS.ForwardTacotron.utils.kannada.cleaners import KannadaCleaner
from TTS.ForwardTacotron.utils.kannada.tokenizer import KannadaTokenizer

import TTS.cargan as cargan

# TTS Paths
cargan_checkpoint_hi_male = "TTS/runs/hindi_male/best_netG.pt"
ft_checkpoint_hi_male = "TTS/ForwardTacotron/checkpoints/hindi_male/latest_model.pt"

cargan_checkpoint_mr_female = "TTS/runs/marathi_female/best_netG.pt"
ft_checkpoint_mr_female = "TTS/ForwardTacotron/checkpoints/marathi_female/latest_model.pt"

cargan_checkpoint_gu_female = "TTS/runs/gujarati_female/best_netG.pt"
ft_checkpoint_gu_female = "TTS/ForwardTacotron/checkpoints/gujarati_female/latest_model.pt"

cargan_checkpoint_kn_female = "TTS/runs/kannada_female/best_netG.pt"
ft_checkpoint_kn_female = "TTS/ForwardTacotron/checkpoints/kannada_female/latest_model.pt"

cargan_checkpoint_bn_female = "TTS/runs/bengali_female/best_netG.pt"
ft_checkpoint_bn_female = "TTS/ForwardTacotron/checkpoints/bengali_female/latest_model.pt"

cargan_checkpoint_bn_male = "TTS/runs/bengali_male/best_netG.pt"
ft_checkpoint_bn_male = "TTS/ForwardTacotron/checkpoints/bengali_male/latest_model.pt"


def Forwardtacotron(text, amp, lang_gen, config, tts_model):
    device = torch.device("cpu")
    if lang_gen == 'mr_female':
        cleaner = MarathiCleaner.from_config(config)
        tokenizer = MarathiTokenizer()
    elif lang_gen == 'hi_male':
        cleaner = HindiCleaner.from_config(config)
        tokenizer = HindiTokenizer()
    elif lang_gen == 'gu_female':
        cleaner = GujaratiCleaner.from_config(config)
        tokenizer = GujaratiTokenizer()
    elif lang_gen == 'kn_female':
        cleaner = KannadaCleaner.from_config(config)
        tokenizer = KannadaTokenizer()
    elif lang_gen == 'bn_male':
        cleaner = BengaliCleaner.from_config(config)
        tokenizer = BengaliTokenizer()
    elif lang_gen == 'bn_female':
        cleaner = BengaliCleaner.from_config(config)
        tokenizer = BengaliTokenizer()

    pitch_function = lambda x: x * amp
    energy_function = lambda x: x

    x = cleaner(text)
    x = tokenizer(x)
    x = torch.as_tensor(x, dtype=torch.long, device=device).unsqueeze(0)

    # if lang == "hi_male":
    #     gen = tts_model_hi_male.generate(x=x,
    #                             alpha=1.,
    #                             pitch_function=pitch_function,
    #                             energy_function=energy_function)
    # elif lang == "mr_female":
    #     gen = tts_model_mr_female.generate(x=x,
    #                             alpha=1.,
    #                             pitch_function=pitch_function,
    #                             energy_function=energy_function)
    # elif lang == "gu_female":
    #     gen = tts_model_gu_female.generate(x=x,
    #                             alpha=1.,
    #                             pitch_function=pitch_function,
    #                             energy_function=energy_function)
    # elif lang == "kn_female":
    #     gen = tts_model_kn_female.generate(x=x,
    #                             alpha=1.,
    #                             pitch_function=pitch_function,
    #                             energy_function=energy_function)
    # elif lang == "bn_female":
    #     gen = tts_model_bn_female.generate(x=x,
    #                             alpha=1.,
    #                             pitch_function=pitch_function,
    #                             energy_function=energy_function)
    # elif lang == "bn_male":
    #     gen = tts_model_bn_male.generate(x=x,
    #                             alpha=1.,
    #                             pitch_function=pitch_function,
    #                             energy_function=energy_function)

    gen = tts_model.generate(x=x,
                             alpha=1.,
                             pitch_function=pitch_function,
                             energy_function=energy_function)
    
    if lang_gen == "mr_female":
        mel_output = gen['mel'] 
    else:
        mel_output = gen['mel_post']

    mel_output = torch.exp(mel_output)
    mel_output = torch.log10(mel_output)

    return mel_output


def Cargan(features, cargan_model):

    # if lang_gen == "mr_female":
    #     with torch.no_grad():
    #         vocoded = cargan.ar_loop(cargan_model_mr_female, features)
    # elif lang_gen == "hi_male":
    #     with torch.no_grad():
    #         vocoded = cargan.ar_loop(cargan_model_hi_male, features)
    # elif lang_gen == "gu_female":
    #     with torch.no_grad():
    #         vocoded = cargan.ar_loop(cargan_model_gu_female, features)
    # elif lang_gen == "kn_female":
    #     with torch.no_grad():
    #         vocoded = cargan.ar_loop(cargan_model_kn_female, features)
    # elif lang_gen == "bn_female":
    #     with torch.no_grad():
    #         vocoded = cargan.ar_loop(cargan_model_bn_female, features)
    # elif lang_gen == "bn_male":
    #     with torch.no_grad():
    #         vocoded = cargan.ar_loop(cargan_model_bn_male, features)

    with torch.no_grad():
        vocoded = cargan.ar_loop(cargan_model, features)

    return vocoded.squeeze(0)

    
def synthesize(text, lang_gen, amp=1.0):
    """
        lang_gen (str): Language of the input text along with gender [gujarati, kannada, marathi, hindi, bengali]
        text (str): Text that needs to be synthesized
    """

    mapping = {
        'Marathi Female': 'mr_female',
        'Hindi Male': 'hi_male',
        'Gujarati Female': 'gu_female',
        'Kannada Female': 'kn_female',
        'Bengali Female': 'bn_female',
        'Bengali Male': 'bn_male'
    }
    lang_gen = mapping[lang_gen]

    if lang_gen=="hi_male":
        # ForwardTacotron
        checkpoint = torch.load(ft_checkpoint_hi_male, map_location=torch.device('cpu'))
        config = checkpoint['config']
        tts_model = ForwardTacotron.from_config(config)
        tts_model.load_state_dict(checkpoint['model'])
        tts_model.eval()
        # Cargan
        cargan_model = cargan.load.model(cargan_checkpoint_hi_male)
    elif lang_gen=="mr_female":
        # ForwardTacotron
        checkpoint = torch.load(ft_checkpoint_mr_female, map_location=torch.device('cpu'))
        config = checkpoint['config']
        tts_model = ForwardTacotron.from_config(config)
        tts_model.load_state_dict(checkpoint['model'])
        tts_model.eval()
        # Cargan
        cargan_model = cargan.load.model(cargan_checkpoint_mr_female)
    elif lang_gen=="gu_female":
        # ForwardTacotron
        checkpoint = torch.load(ft_checkpoint_gu_female, map_location=torch.device('cpu'))
        config = checkpoint['config']
        tts_model = ForwardTacotron.from_config(config)
        tts_model.load_state_dict(checkpoint['model'])
        tts_model.eval()
        # Cargan
        cargan_model = cargan.load.model(cargan_checkpoint_gu_female)
    elif lang_gen=="kn_female":
        # ForwardTacotron
        checkpoint = torch.load(ft_checkpoint_kn_female, map_location=torch.device('cpu'))
        config = checkpoint['config']
        tts_model = ForwardTacotron.from_config(config)
        tts_model.load_state_dict(checkpoint['model'])
        tts_model.eval()
        # Cargan
        cargan_model = cargan.load.model(cargan_checkpoint_kn_female)
    elif lang_gen=="bn_female":
        # ForwardTacotron
        checkpoint = torch.load(ft_checkpoint_bn_female, map_location=torch.device('cpu'))
        config = checkpoint['config']
        tts_model = ForwardTacotron.from_config(config)
        tts_model.load_state_dict(checkpoint['model'])
        tts_model.eval()
        # Cargan
        cargan_model = cargan.load.model(cargan_checkpoint_bn_female)
    elif lang_gen=="bn_male":
        # ForwardTacotron
        checkpoint = torch.load(ft_checkpoint_bn_male, map_location=torch.device('cpu'))
        config = checkpoint['config']
        tts_model = ForwardTacotron.from_config(config)
        tts_model.load_state_dict(checkpoint['model'])
        tts_model.eval()
        # Cargan
        cargan_model = cargan.load.model(cargan_checkpoint_bn_male)

    # mel spectrogram file generated by the text-to-mel model
    mel_output = Forwardtacotron(text, amp, lang_gen, config, tts_model)

    # variable vocoded is the final generated speech
    vocoded = Cargan(mel_output, cargan_model).squeeze().cpu().numpy()

    return 22050, vocoded


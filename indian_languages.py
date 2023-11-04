import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa
import sys,os

def transcript(audio_path,model):
    DEVICE_ID = "cpu"
    torch.cuda.empty_cache()
    MODEL_ID = model

    audio_data, s_r = load_audio_file(audio_path)
    processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)

    model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID).to(DEVICE_ID)

    input_features = processor(audio_data, sampling_rate=s_r, return_tensors="pt", padding=True)

    with torch.no_grad():
        logits = model(input_features.input_values.to(DEVICE_ID)).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    predicted_sentence = processor.batch_decode(predicted_ids)[0]

    tokens = predicted_sentence.split()
    timestamps = calculate_word_timestamps(audio_data, s_r, tokens)

    # for token, start_time, end_time in timestamps:
    #     print(f"Word: {token}, Start Time: {start_time}, End Time: {end_time}")

    return timestamps

def load_audio_file(audio_path):
    speech_array, s_r = librosa.load(audio_path, sr=16_000)
    return speech_array, s_r

def calculate_word_timestamps(audio_data, s_r, tokens):
    timestamps = []
    frame_duration = len(audio_data) / (len(tokens) * s_r)
    start_time = 0.0

    for token in tokens:
        end_time = start_time + frame_duration
        timestamps.append((token, start_time, end_time))
        start_time = end_time

    return timestamps

dirs = sys.argv[1]
model = sys.argv[2]
dir_list = os.listdir(dirs + "/audio/mp3/waves/")
file_name = dirs + "/text.txt"
wfile = open(file_name, 'w', encoding='utf-8')
ts = []
count = 0
for y in dir_list:
    x = dirs + "/audio/mp3/waves/" + y
    if x.endswith(".wav"):
        count += 1
    else:
        continue

    y = transcript(x,model)
    print(x)
    print(y)
    ts.append(x + "\t" + str(y) + "\n")
print(count)

ts.sort()
for i in ts:
    wfile.write(i)
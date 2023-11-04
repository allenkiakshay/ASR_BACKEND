import whisperx
import gc 
import json
import sys

import gc
import torch
torch.cuda.empty_cache()
gc.collect()

device = "cpu"
print(device)
audio_file = sys.argv[1]
dir = sys.argv[2]
batch_size = 16 # reduce if low on GPU mem
compute_type = "float32" # change to "int8" if low on GPU mem (may reduce accuracy)


# 1. Transcribe with original whis
# per (batched)
model = whisperx.load_model("large-v2", device, compute_type=compute_type)
audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
print(result["language"]) # before alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
#model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
model_a, metadata = whisperx.load_align_model(language_code="en", device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
print(len(result["segments"]))
# print(result["segments"])

############################################################################################################
# 3. Assign speaker labels
diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)

# add min/max number of speakers if known
diarize_segments = diarize_model(audio_file, min_speakers=1, max_speakers=3)


result = whisperx.assign_word_speakers(diarize_segments, result)
#print(diarize_segments)
print(result["segments"]) # segments are now assigned speaker IDs

##################################################################################################################
file_name = dir+"/transcript.xml"
wfile = open(file_name, 'w+', encoding='utf-8')
file_name = dir+"/text.txt"
#file_name = dir+"/text"+audio_file+".txt"
yfile = open(file_name, 'w+', encoding='utf-8')

i = 0

wfile.write('<?xml version="1.0" encoding="UTF-8"?>'+"\n")
wfile.write('<transcript lang="english">'+"\n")
for i in range(len(result["segments"])):
	times = float(result["segments"][i]["end"])
	speaker = str(result["segments"][i]["speaker"])
	yfile.write(str(result["segments"][i]["text"])+"\t"+str(result["segments"][i]["end"])+"\n")
	hr = int(times/3600)
	min = int((times-hr*3600)/60)
	sec = round(times - hr*3600 - min*60,2)
	if hr < 10:
		if min < 10:
			if sec < 10:
				time = str("0"+str(hr)+":0"+str(min)+":0"+str(sec))
			else:
				time = str("0"+str(hr)+":0"+str(min)+":"+str(sec))
		else:
			if sec < 10:
				time = str("0"+str(hr)+":"+str(min)+":0"+str(sec))
			else:
				time = str("0"+str(hr)+":"+str(min)+":"+str(sec))
	else:
		if min < 10:
			if sec < 10:
				time = str(str(hr)+":0"+str(min)+":0"+str(sec))
			else:
				time = str(str(hr)+":0"+str(min)+":"+str(sec))
		else:
			if sec < 10:
				time = str(str(hr)+":"+str(min)+":0"+str(sec))
			else:
				time = str(str(hr)+":"+str(min)+":"+str(sec))
	#wfile.write("<line timestamp=\""+str(time)+"\" speaker=\"Speaker_1\">"+"\n")
	wfile.write("<line timestamp=\""+str(time)+"\" speaker=\""+speaker+"\">"+"\n")
	#print(result["segments"][i]["words"])
	for j in range(len(result["segments"][i]["words"])):
		#print(result["segments"][0]["words"]) # after alignment
		#print(result["segments"][i]["words"][j]["word"],result["segments"][i]["words"][j]["start"],result["segments"][i]["words"][j]["end"])
		word = result["segments"][i]["words"][j]["word"]
		if "end" in result["segments"][i]["words"][j]:
			word_time = float(result["segments"][i]["words"][j]["end"])
			hr = int(word_time/3600)
			min = int((word_time-hr*3600)/60)
			sec = round(word_time - hr*3600 - min*60,2)

			if hr < 10:
				if min < 10:
					if sec < 10:
						time = str("0"+str(hr)+":0"+str(min)+":0"+str(sec))
					else:
						time = str("0"+str(hr)+":0"+str(min)+":"+str(sec))
				else:
					if sec < 10:
						time = str("0"+str(hr)+":"+str(min)+":0"+str(sec))
					else:
						time = str("0"+str(hr)+":"+str(min)+":"+str(sec))
			else:
				if min < 10:
					if sec < 10:
						time = str(str(hr)+":0"+str(min)+":0"+str(sec))
					else:
						time = str(str(hr)+":0"+str(min)+":"+str(sec))
				else:
					if sec < 10:
						time = str(str(hr)+":"+str(min)+":0"+str(sec))
					else:
						time = str(str(hr)+":"+str(min)+":"+str(sec))
			wfile.write("<word timestamp=\""+str(time)+"\" is_valid=\"1\">"+str(word)+"</word>"+"\n")
		else:
			wfile.write("<word timestamp=\"\" is_valid=\"1\">"+str(word)+"</word>"+"\n")
	wfile.write("</line>"+"\n")
wfile.write('</transcript>')




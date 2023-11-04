import os
import sys
from scipy.io.wavfile import write
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

#print("Hello World")

from tts import synthesize

text = sys.argv[1] 
lang = sys.argv[2]  # 'Hindi Male' # Other options - 'Marathi Female', 'Gujarati Female', 'Kannada Female', 'Bengali Female', 'Bengali Male'
output_file=sys.argv[3]
sr,y = synthesize(text,lang)

write(output_file, sr, y)




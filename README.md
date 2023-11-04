# Install The Requirements
  - command: sudo apt install ffmpeg mp3splt sox libsox-fmt-mp3 redis -y
  - command: pip install flask
  - command: pip install librosa
  - command: pip install pytorch
  - command: pip install torchvision
  - command: pip install nltk
  - command: pip install ffmpeg-python
  - command: pip install pyannote.audio
  - command: pip install transformers
  - command: pip install celery[redis]
  - command: pip install faster_whisper
  - command: pip install ctranslate2
# To start server run these commands
  - command: rm -rf ./uploads
  - command: python main.py
  - command: celery -A tasks worker --loglevel=info

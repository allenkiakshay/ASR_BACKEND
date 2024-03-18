# Install The Requirements

```
pip install flask
pip install Flask-Cors
pip install librosa
pip install torch
pip install torchvision
pip install nltk
pip install ffmpeg-python
pip install pyannote.audio
pip install transformers
pip install celery[redis]
pip install faster_whisper
pip install ctranslate2
pip install pydub
```

# To start server run these commands

- command: rm -rf ./uploads
- command: python wsgi.py
- command: celery -A tasks worker --loglevel=info

# To start server run these commands
  - command: rm -rf ./uploads
  - command: python main.py
  - command: celery -A tasks worker --loglevel=info

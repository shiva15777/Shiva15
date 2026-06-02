import os
from datetime import timedelta

# Flask Configuration
DEBUG = True
TESTING = False

# Upload Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg', 'm4a'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

# Audio Processing Configuration
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_HOP_LENGTH = 512
AUDIO_FORMAT = 'mp3'
AUDIO_BITRATE = '192k'

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Temporary directory for processing
TEMP_FOLDER = 'temp'
os.makedirs(TEMP_FOLDER, exist_ok=True)
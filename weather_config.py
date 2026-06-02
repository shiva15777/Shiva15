import os
from datetime import timedelta

# Flask Configuration
DEBUG = True
TESTING = False

# Weather API Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'YOUR_API_KEY_HERE')
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5'

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Cache Configuration
CACHE_FOLDER = 'cache'
CACHE_TIMEOUT = 600  # 10 minutes

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///weather.db')

# Create directories if they don't exist
os.makedirs(CACHE_FOLDER, exist_ok=True)

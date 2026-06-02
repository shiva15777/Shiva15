@echo off
REM Auto-setup script for Windows
REM Run this from the Shiva15 directory

echo.
echo 🚀 Setting up Shiva15 apps...
echo.

echo 📦 Installing Python packages...
pip install Flask Flask-CORS requests librosa soundfile pydub numpy scipy python-dotenv

echo.
echo Creating necessary directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs
if not exist "temp" mkdir temp
if not exist "cache" mkdir cache

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Get API key from: https://openweathermap.org
echo 2. Run Audio Master: python app.py
echo 3. Run Weather (in another cmd): python weather_app.py
echo 4. Open To-Do: Open todo_list.html in browser
echo.
echo Happy coding! 🎉
echo.
pause

# 🎵 Hermus - Audio Processing Tool

A free, open-source audio processing application that helps you upload audio files, analyze them, sync lyrics with beats, and export high-quality MP3 files.

## 🌟 Features

- 🎤 **Audio Upload**: Upload MP3, WAV, FLAC, OGG, and M4A files
- 🎼 **Audio Analysis**: Detect beats, tempo, and musical characteristics
- 📝 **Lyrics Sync**: Synchronize lyrics with music beats
- 🎚️ **Audio Mastering**: Normalization and audio processing
- 📤 **MP3 Export**: Export processed audio as MP3
- 💯 **100% Free**: No watermarks, no limits, open-source
- 🎨 **Beautiful UI**: Modern, responsive web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- FFmpeg (for audio conversion)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shiva15777/Shiva15.git
   cd Shiva15
   ```

2. **Install FFmpeg**
   - **Windows**: Download from https://ffmpeg.org/download.html or use `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

3. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📋 How to Use

### Step 1: Upload Audio
- Click the upload area or drag-and-drop an audio file
- Supported formats: MP3, WAV, FLAC, OGG, M4A
- Max file size: 100 MB

### Step 2: Analyze Audio
- Click "Analyze Audio"
- View tempo, beats, and spectral features

### Step 3: Add Lyrics
- Enter or paste lyrics (one line per line)
- Click "Sync Lyrics to Beats"
- Review the timing data

### Step 4: Master Audio
- Choose normalization settings
- Set target loudness (LUFS)
- Optionally apply compression
- Click "Master Audio"

### Step 5: Export
- Click "Export as MP3"
- Download your processed audio file

## 📦 Project Structure

```
Hermus/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── .gitignore                  # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── main.js            # Frontend logic
├── templates/
│   └── index.html             # Main HTML page
├── utils/
│   ├── __init__.py            # Package init
│   ├── audio_processor.py     # Audio analysis functions
│   ├── lyrics_sync.py         # Lyrics synchronization
│   └── audio_master.py        # Audio mastering functions
├── uploads/                   # User uploaded files
├── outputs/                   # Processed output files
└── temp/                      # Temporary files
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Audio settings
DEFAULT_SAMPLE_RATE = 44100  # Sampling rate
DEFAULT_HOP_LENGTH = 512     # Frame length for analysis
AUDIO_FORMAT = 'mp3'         # Output format
AUDIO_BITRATE = '192k'       # MP3 bitrate

# Upload settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac', 'ogg', 'm4a'}

# Paths
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
TEMP_FOLDER = 'temp'
```

## 🐛 Troubleshooting

### FFmpeg not found
- **Solution**: Install FFmpeg and add it to your system PATH

### "No module named librosa"
- **Solution**: Run `pip install -r requirements.txt`

### Port 5000 already in use
- **Solution**: Edit `app.py` and change `port=5000` to another port

### Audio file not recognized
- **Solution**: Ensure your audio file is in a supported format and FFmpeg is installed

## 📚 API Reference

### Upload Audio
**POST** `/api/upload`
```json
{
  "file": "audio file"
}
```

### Analyze Audio
**POST** `/api/analyze`
```json
{
  "filepath": "uploads/song.mp3"
}
```

### Sync Lyrics
**POST** `/api/sync-lyrics`
```json
{
  "filepath": "uploads/song.mp3",
  "lyrics": "Line 1\nLine 2\nLine 3"
}
```

### Master Audio
**POST** `/api/process`
```json
{
  "filepath": "uploads/song.mp3",
  "normalize": true,
  "loudness": -14
}
```

### Export as MP3
**POST** `/api/export`
```json
{
  "filepath": "temp/song_mastered.wav"
}
```

### Download File
**GET** `/api/download/<filename>`

## 🎓 Technologies Used

- **Backend**: Python 3.9+ with Flask
- **Audio Processing**: Librosa, SoundFile, Pydub
- **Frontend**: HTML5, CSS3, JavaScript
- **Audio Conversion**: FFmpeg

## 🚀 Future Enhancements

- [ ] Batch processing
- [ ] Vocal extraction
- [ ] Genre detection
- [ ] Automatic lyrics generation (with Genius API)
- [ ] Waveform visualization
- [ ] Real-time audio preview
- [ ] Advanced EQ and effects
- [ ] Audio effects (reverb, delay, echo)
- [ ] Multitrack support
- [ ] Desktop app (Electron)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 💬 Support

Have questions or issues?
- Open an issue on GitHub
- Check existing issues for solutions
- Submit a discussion

## 🙏 Acknowledgments

- [Librosa](https://librosa.org/) - Audio analysis library
- [Pydub](https://github.com/jiaaro/pydub) - Audio processing
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [FFmpeg](https://ffmpeg.org/) - Audio conversion

## 📞 Contact

Created with ❤️ by [shiva15777](https://github.com/shiva15777)

**GitHub**: https://github.com/shiva15777/Shiva15
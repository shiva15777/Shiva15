from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import logging

from config import *
from utils.audio_processor import AudioProcessor
from utils.lyrics_sync import LyricsSync
from utils.audio_master import AudioMaster

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config')
CORS(app)

# Initialize processors
audio_processor = AudioProcessor()
lyrics_sync = LyricsSync()
audio_master = AudioMaster()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'File too large. Maximum: {MAX_FILE_SIZE / 1024 / 1024:.0f}MB'}), 400

        # Save file
        timestamp = get_timestamp()
        filename = secure_filename(f"{timestamp}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        logger.info(f"File uploaded: {filename}")

        return jsonify({
            'success': True,
            'file_id': timestamp,
            'filename': filename,
            'filepath': filepath
        }), 200

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_audio():
    """Analyze uploaded audio file"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        logger.info(f"Analyzing: {filepath}")

        # Analyze audio
        analysis = audio_processor.analyze(filepath)

        return jsonify({
            'success': True,
            'analysis': analysis
        }), 200

    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sync-lyrics', methods=['POST'])
def sync_lyrics():
    """Sync lyrics with audio"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        lyrics_text = data.get('lyrics', '')

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        if not lyrics_text:
            return jsonify({'error': 'No lyrics provided'}), 400

        logger.info(f"Syncing lyrics for: {filepath}")

        # Sync lyrics
        sync_data = lyrics_sync.sync_to_beats(filepath, lyrics_text)

        return jsonify({
            'success': True,
            'sync_data': sync_data
        }), 200

    except Exception as e:
        logger.error(f"Lyrics sync error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_audio():
    """Process and master audio"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')
        normalize = data.get('normalize', True)
        loudness = data.get('loudness', -14)

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        logger.info(f"Processing: {filepath}")

        # Master audio
        output_path = audio_master.master(filepath, normalize=normalize, loudness=loudness)

        return jsonify({
            'success': True,
            'output_path': output_path,
            'output_filename': os.path.basename(output_path)
        }), 200

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_audio():
    """Export processed audio as MP3"""
    try:
        data = request.get_json()
        filepath = data.get('filepath')

        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        logger.info(f"Exporting: {filepath}")

        # Export as MP3
        output_path = audio_master.export_mp3(filepath)

        return jsonify({
            'success': True,
            'output_path': output_path,
            'output_filename': os.path.basename(output_path),
            'download_url': f'/api/download/{os.path.basename(output_path)}'
        }), 200

    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download processed file"""
    try:
        filepath = os.path.join(OUTPUT_FOLDER, secure_filename(filename))

        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status/<job_id>', methods=['GET'])
def check_status(job_id):
    """Check processing status"""
    try:
        # This is a placeholder for job status tracking
        # In production, use a task queue like Celery

        return jsonify({
            'job_id': job_id,
            'status': 'completed',
            'progress': 100
        }), 200

    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)

import librosa
import numpy as np
import json
import logging

logger = logging.getLogger(__name__)

class LyricsSync:
    """Handle lyrics synchronization with audio"""
    
    def __init__(self):
        self.sr = 44100
        self.hop_length = 512
    
    def sync_to_beats(self, filepath, lyrics_text):
        """Sync lyrics to audio beats"""
        try:
            # Load audio
            y, sr = librosa.load(filepath, sr=self.sr)
            
            # Detect beats
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
            
            # Convert beat frames to time
            beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=self.hop_length)
            
            # Split lyrics into lines
            lyrics_lines = [line.strip() for line in lyrics_text.split('\n') if line.strip()]
            
            # Sync lyrics to beats
            sync_data = []
            for i, lyric in enumerate(lyrics_lines):
                if i < len(beat_times):
                    sync_data.append({
                        'line': i + 1,
                        'text': lyric,
                        'time': float(beat_times[i]),
                        'beat': int(i)
                    })
            
            logger.info(f"Synced {len(sync_data)} lyrics lines")
            return sync_data
            
        except Exception as e:
            logger.error(f"Lyrics sync error: {str(e)}")
            raise
    
    def generate_srt(self, sync_data, output_path):
        """Generate SRT subtitle file from sync data"""
        try:
            srt_content = ""
            for i, item in enumerate(sync_data, 1):
                start_time = self._seconds_to_srt_time(item['time'])
                
                # Estimate end time (next beat or +2 seconds)
                if i < len(sync_data):
                    end_time = self._seconds_to_srt_time(sync_data[i]['time'])
                else:
                    end_time = self._seconds_to_srt_time(item['time'] + 2)
                
                srt_content += f"{i}\n{start_time} --> {end_time}\n{item['text']}\n\n"
            
            with open(output_path, 'w') as f:
                f.write(srt_content)
            
            logger.info(f"SRT file generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"SRT generation error: {str(e)}")
            raise
    
    @staticmethod
    def _seconds_to_srt_time(seconds):
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

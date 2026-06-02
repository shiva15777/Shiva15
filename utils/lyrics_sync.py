import numpy as np
import librosa
from config import DEFAULT_SAMPLE_RATE, DEFAULT_HOP_LENGTH
import logging

logger = logging.getLogger(__name__)


class LyricsSync:
    """Synchronize lyrics with audio beats"""

    def __init__(self, sample_rate=DEFAULT_SAMPLE_RATE, hop_length=DEFAULT_HOP_LENGTH):
        self.sample_rate = sample_rate
        self.hop_length = hop_length

    def sync_to_beats(self, filepath, lyrics_text):
        """Sync lyrics text to detected beats"""
        try:
            logger.info(f"Syncing lyrics to: {filepath}")
            
            # Load audio
            y, sr = librosa.load(filepath, sr=self.sample_rate)
            
            # Detect beats
            _, beats = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            # Split lyrics by lines
            lines = [line.strip() for line in lyrics_text.split('\n') if line.strip()]
            
            # Create sync data
            sync_data = []
            
            # Distribute lyrics across beats
            beats_per_line = max(1, len(beat_times) // len(lines)) if lines else 1
            
            for i, line in enumerate(lines):
                start_beat = i * beats_per_line
                if start_beat < len(beat_times):
                    start_time = float(beat_times[start_beat])
                    
                    # Calculate end time
                    end_beat = min(start_beat + beats_per_line, len(beat_times) - 1)
                    if end_beat < len(beat_times):
                        end_time = float(beat_times[end_beat])
                    else:
                        end_time = float(librosa.get_duration(y=y, sr=sr))
                    
                    sync_data.append({
                        'line_index': i,
                        'text': line,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time
                    })
            
            logger.info(f"Synced {len(sync_data)} lines to beats")
            return sync_data

        except Exception as e:
            logger.error(f"Error syncing lyrics: {str(e)}")
            raise

    def align_lyrics_to_onsets(self, filepath, lyrics_text):
        """Align lyrics to detected onset times"""
        try:
            logger.info(f"Aligning lyrics to onsets: {filepath}")
            
            # Load audio
            y, sr = librosa.load(filepath, sr=self.sample_rate)
            
            # Detect onsets
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            onset_frames = librosa.onset.onset_detect(
                onset_env=onset_env,
                sr=sr,
                units='time'
            )
            
            # Split lyrics
            lines = [line.strip() for line in lyrics_text.split('\n') if line.strip()]
            
            # Align lyrics to onsets
            sync_data = []
            for i, line in enumerate(lines):
                if i < len(onset_frames):
                    start_time = float(onset_frames[i])
                    
                    # Calculate end time
                    if i + 1 < len(onset_frames):
                        end_time = float(onset_frames[i + 1])
                    else:
                        end_time = float(librosa.get_duration(y=y, sr=sr))
                    
                    sync_data.append({
                        'line_index': i,
                        'text': line,
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': end_time - start_time
                    })
            
            logger.info(f"Aligned {len(sync_data)} lines to onsets")
            return sync_data

        except Exception as e:
            logger.error(f"Error aligning lyrics: {str(e)}")
            raise

    def create_karaoke_data(self, filepath, lyrics_text):
        """Create karaoke-style timing data for lyrics"""
        try:
            # Get beat-based sync
            sync_data = self.sync_to_beats(filepath, lyrics_text)
            
            # Format as karaoke data
            karaoke_data = {
                'lyrics': [item['text'] for item in sync_data],
                'timings': [
                    {
                        'start': item['start_time'],
                        'end': item['end_time'],
                        'text': item['text']
                    }
                    for item in sync_data
                ]
            }
            
            return karaoke_data

        except Exception as e:
            logger.error(f"Error creating karaoke data: {str(e)}")
            raise
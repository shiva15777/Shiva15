import librosa
import numpy as np
import soundfile as sf
from config import DEFAULT_SAMPLE_RATE, DEFAULT_HOP_LENGTH
import logging

logger = logging.getLogger(__name__)


class AudioProcessor:
    """Handle audio analysis and processing"""

    def __init__(self, sample_rate=DEFAULT_SAMPLE_RATE, hop_length=DEFAULT_HOP_LENGTH):
        self.sample_rate = sample_rate
        self.hop_length = hop_length

    def analyze(self, filepath):
        """Analyze audio file and extract features"""
        try:
            logger.info(f"Loading audio: {filepath}")
            
            # Load audio file
            y, sr = librosa.load(filepath, sr=self.sample_rate)
            
            # Get duration
            duration = librosa.get_duration(y=y, sr=sr)
            
            # Detect tempo and beats
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
            beat_times = librosa.frames_to_time(beats, sr=sr)
            
            # Extract spectral features
            S = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=self.hop_length)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)
            
            # RMS energy
            rms = librosa.feature.rms(y=y)
            
            # MFCC
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            analysis = {
                'duration': float(duration),
                'sample_rate': int(sr),
                'tempo': float(tempo),
                'beats_count': int(len(beats)),
                'beat_times': [float(t) for t in beat_times[:20]],  # First 20 beats
                'spectral_centroid_mean': float(np.mean(spectral_centroid)),
                'spectral_rolloff_mean': float(np.mean(spectral_rolloff)),
                'zero_crossing_rate_mean': float(np.mean(zcr)),
                'rms_energy_mean': float(np.mean(rms)),
                'mfcc_mean': [float(x) for x in np.mean(mfcc, axis=1)]
            }
            
            logger.info(f"Analysis complete. Tempo: {tempo:.1f} BPM, Duration: {duration:.2f}s")
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing audio: {str(e)}")
            raise

    def detect_onset_times(self, filepath):
        """Detect onset times in audio"""
        try:
            y, sr = librosa.load(filepath, sr=self.sample_rate)
            
            # Detect onsets
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            onset_frames = librosa.onset.onset_detect(
                onset_env=onset_env,
                sr=sr,
                units='time'
            )
            
            return [float(t) for t in onset_frames]

        except Exception as e:
            logger.error(f"Error detecting onsets: {str(e)}")
            raise

    def extract_chroma(self, filepath):
        """Extract chroma features"""
        try:
            y, sr = librosa.load(filepath, sr=self.sample_rate)
            
            chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
            chroma_mean = np.mean(chroma, axis=1)
            
            return [float(x) for x in chroma_mean]

        except Exception as e:
            logger.error(f"Error extracting chroma: {str(e)}")
            raise

    def get_audio_info(self, filepath):
        """Get basic audio file information"""
        try:
            y, sr = librosa.load(filepath, sr=self.sample_rate)
            duration = librosa.get_duration(y=y, sr=sr)
            
            return {
                'sample_rate': int(sr),
                'duration': float(duration),
                'num_samples': int(len(y)),
                'channels': 1  # Mono after librosa.load
            }

        except Exception as e:
            logger.error(f"Error getting audio info: {str(e)}")
            raise
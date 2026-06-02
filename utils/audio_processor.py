import librosa
import numpy as np
import soundfile as sf
from scipy.fftpack import fft
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handle audio analysis and processing"""
    
    def __init__(self):
        self.sr = 44100
        self.hop_length = 512
    
    def analyze(self, filepath):
        """Analyze audio file and return metrics"""
        try:
            # Load audio
            y, sr = librosa.load(filepath, sr=self.sr)
            
            # Calculate metrics
            duration = librosa.get_duration(y=y, sr=sr)
            rms = float(np.sqrt(np.mean(y**2)))
            loudness = float(20 * np.log10(rms + 1e-9))
            
            # Detect beat
            onset_env = librosa.onset.onset_strength(y=y, sr=sr)
            tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=self.hop_length)
            
            # Spectral features
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            analysis = {
                'duration': float(duration),
                'sample_rate': int(sr),
                'rms_energy': float(rms),
                'loudness_db': float(loudness),
                'tempo': float(tempo),
                'spectral_centroid_mean': float(np.mean(spectral_centroid)),
                'spectral_centroid_std': float(np.std(spectral_centroid)),
                'mfcc_mean': float(np.mean(mfcc)),
                'total_samples': len(y)
            }
            
            logger.info(f"Analysis complete: {analysis}")
            return analysis
            
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise
    
    def normalize_audio(self, y, target_loudness=-14):
        """Normalize audio to target loudness"""
        try:
            # Calculate current loudness
            rms = np.sqrt(np.mean(y**2))
            current_loudness = 20 * np.log10(rms + 1e-9)
            
            # Calculate gain
            gain_db = target_loudness - current_loudness
            gain_linear = 10 ** (gain_db / 20)
            
            # Apply gain
            normalized = y * gain_linear
            
            # Prevent clipping
            max_val = np.max(np.abs(normalized))
            if max_val > 1.0:
                normalized = normalized / max_val
            
            return normalized
            
        except Exception as e:
            logger.error(f"Normalization error: {str(e)}")
            raise

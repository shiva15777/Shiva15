import librosa
import soundfile as sf
import numpy as np
import os
from pydub import AudioSegment
from scipy import signal
import logging
from config import OUTPUT_FOLDER, TEMP_FOLDER, AUDIO_BITRATE

logger = logging.getLogger(__name__)

class AudioMaster:
    """Handle audio mastering and processing"""
    
    def __init__(self):
        self.sr = 44100
        self.hop_length = 512
    
    def master(self, filepath, normalize=True, loudness=-14):
        """Master audio with compression, EQ, and normalization"""
        try:
            logger.info(f"Starting mastering: {filepath}")
            
            # Load audio
            y, sr = librosa.load(filepath, sr=self.sr)
            
            # Apply processing chain
            y = self._apply_eq(y, sr)
            y = self._apply_compression(y, sr)
            
            if normalize:
                y = self._normalize(y, loudness)
            
            # Apply limiting to prevent clipping
            y = self._apply_limiter(y)
            
            # Generate output filename
            base_name = os.path.basename(filepath)
            name_without_ext = os.path.splitext(base_name)[0]
            output_filename = f"{name_without_ext}_mastered.wav"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            # Save mastered audio
            sf.write(output_path, y, sr)
            logger.info(f"Mastered audio saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Mastering error: {str(e)}")
            raise
    
    def export_mp3(self, filepath, bitrate=AUDIO_BITRATE):
        """Export audio as MP3"""
        try:
            logger.info(f"Exporting to MP3: {filepath}")
            
            # Load audio file
            audio = AudioSegment.from_wav(filepath)
            
            # Generate output filename
            base_name = os.path.basename(filepath)
            name_without_ext = os.path.splitext(base_name)[0]
            output_filename = f"{name_without_ext}.mp3"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            # Export as MP3
            audio.export(output_path, format="mp3", bitrate=bitrate)
            logger.info(f"MP3 exported: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"MP3 export error: {str(e)}")
            raise
    
    def _apply_eq(self, y, sr):
        """Apply equalization to audio"""
        try:
            # Simple 3-band EQ
            # Low shelf filter (boost bass)
            sos_low = signal.butter(2, 200, btype='low', fs=sr, output='sos')
            y_low = signal.sosfilt(sos_low, y) * 0.9
            
            # High shelf filter (boost treble)
            sos_high = signal.butter(2, 5000, btype='high', fs=sr, output='sos')
            y_high = signal.sosfilt(sos_high, y) * 0.8
            
            # Mix
            y = y + y_low * 0.1 + y_high * 0.1
            
            # Normalize to prevent clipping
            max_val = np.max(np.abs(y))
            if max_val > 1.0:
                y = y / max_val
            
            return y
            
        except Exception as e:
            logger.error(f"EQ error: {str(e)}")
            return y
    
    def _apply_compression(self, y, sr, threshold=-20, ratio=4):
        """Apply dynamic range compression"""
        try:
            # Convert to dB
            y_db = 20 * np.log10(np.abs(y) + 1e-9)
            
            # Apply compression
            mask = y_db > threshold
            y_db[mask] = threshold + (y_db[mask] - threshold) / ratio
            
            # Convert back to linear
            y_compressed = np.sign(y) * (10 ** (y_db / 20))
            
            return y_compressed
            
        except Exception as e:
            logger.error(f"Compression error: {str(e)}")
            return y
    
    def _normalize(self, y, target_loudness=-14):
        """Normalize audio to target loudness (LUFS)"""
        try:
            # Calculate current loudness
            rms = np.sqrt(np.mean(y**2))
            current_loudness = 20 * np.log10(rms + 1e-9)
            
            # Calculate gain needed
            gain_db = target_loudness - current_loudness
            gain_linear = 10 ** (gain_db / 20)
            
            # Apply gain
            y_normalized = y * gain_linear
            
            # Prevent clipping
            max_val = np.max(np.abs(y_normalized))
            if max_val > 1.0:
                y_normalized = y_normalized / max_val
            
            logger.info(f"Normalized from {current_loudness:.1f}dB to {target_loudness:.1f}dB")
            return y_normalized
            
        except Exception as e:
            logger.error(f"Normalization error: {str(e)}")
            return y
    
    def _apply_limiter(self, y, threshold=0.95):
        """Apply limiter to prevent clipping"""
        try:
            y_limited = np.clip(y, -threshold, threshold)
            return y_limited
        except Exception as e:
            logger.error(f"Limiter error: {str(e)}")
            return y
    
    def get_processing_stats(self, original_path, processed_path):
        """Get statistics comparing original and processed audio"""
        try:
            y_orig, sr_orig = librosa.load(original_path, sr=self.sr)
            y_proc, sr_proc = librosa.load(processed_path, sr=self.sr)
            
            orig_rms = np.sqrt(np.mean(y_orig**2))
            proc_rms = np.sqrt(np.mean(y_proc**2))
            
            stats = {
                'original_loudness_db': float(20 * np.log10(orig_rms + 1e-9)),
                'processed_loudness_db': float(20 * np.log10(proc_rms + 1e-9)),
                'gain_applied_db': float(20 * np.log10((proc_rms + 1e-9) / (orig_rms + 1e-9))),
                'original_peak': float(np.max(np.abs(y_orig))),
                'processed_peak': float(np.max(np.abs(y_proc)))
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Stats error: {str(e)}")
            raise

import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os
from config import DEFAULT_SAMPLE_RATE, OUTPUT_FOLDER, AUDIO_FORMAT, AUDIO_BITRATE, TEMP_FOLDER
import logging

logger = logging.getLogger(__name__)


class AudioMaster:
    """Handle audio mastering and export"""

    def __init__(self, sample_rate=DEFAULT_SAMPLE_RATE):
        self.sample_rate = sample_rate

    def normalize_audio(self, y, target_loudness=-14):
        """Normalize audio to target loudness (LUFS)"""
        try:
            # Calculate current RMS
            rms = np.sqrt(np.mean(y ** 2))
            
            if rms == 0:
                return y
            
            # Convert target LUFS to linear gain
            # Simplified: -14 LUFS ≈ -14dB
            target_db = target_loudness
            current_db = 20 * np.log10(rms) if rms > 0 else -np.inf
            
            gain_db = target_db - current_db
            gain_linear = 10 ** (gain_db / 20)
            
            # Apply gain with soft clipping to prevent distortion
            y_normalized = y * gain_linear
            
            # Soft clipping
            threshold = 0.95
            mask = np.abs(y_normalized) > threshold
            y_normalized[mask] = np.sign(y_normalized[mask]) * threshold
            
            logger.info(f"Audio normalized. Gain: {gain_db:.2f}dB")
            return y_normalized

        except Exception as e:
            logger.error(f"Error normalizing audio: {str(e)}")
            raise

    def apply_eq(self, y, sr, eq_type='flat'):
        """Apply EQ to audio"""
        try:
            if eq_type == 'bass_boost':
                # Simple bass boost using filtering
                # This is a placeholder - in production use scipy.signal
                logger.info("Applying bass boost")
                return y
            elif eq_type == 'treble_boost':
                logger.info("Applying treble boost")
                return y
            else:
                logger.info("No EQ applied")
                return y

        except Exception as e:
            logger.error(f"Error applying EQ: {str(e)}")
            raise

    def compress_audio(self, y, ratio=4, threshold=0.5):
        """Apply dynamic range compression"""
        try:
            # Simple compressor
            mask = np.abs(y) > threshold
            y_compressed = y.copy()
            y_compressed[mask] = np.sign(y[mask]) * (threshold + (np.abs(y[mask]) - threshold) / ratio)
            
            logger.info(f"Compression applied. Ratio: {ratio}:1, Threshold: {threshold}")
            return y_compressed

        except Exception as e:
            logger.error(f"Error compressing audio: {str(e)}")
            raise

    def master(self, input_path, normalize=True, loudness=-14, compress=False, eq_type='flat'):
        """Master audio file"""
        try:
            logger.info(f"Starting mastering: {input_path}")
            
            # Load audio
            y, sr = librosa.load(input_path, sr=self.sample_rate)
            
            # Apply compression if requested
            if compress:
                y = self.compress_audio(y, ratio=4, threshold=0.5)
            
            # Apply EQ
            y = self.apply_eq(y, sr, eq_type)
            
            # Normalize
            if normalize:
                y = self.normalize_audio(y, target_loudness=loudness)
            
            # Save to temp file
            output_filename = os.path.basename(input_path).split('.')[0] + '_mastered.wav'
            output_path = os.path.join(TEMP_FOLDER, output_filename)
            
            sf.write(output_path, y, sr)
            logger.info(f"Mastering complete: {output_path}")
            
            return output_path

        except Exception as e:
            logger.error(f"Error mastering audio: {str(e)}")
            raise

    def export_mp3(self, input_path, output_folder=OUTPUT_FOLDER, bitrate=AUDIO_BITRATE):
        """Export audio as MP3"""
        try:
            logger.info(f"Exporting to MP3: {input_path}")
            
            # Generate output filename
            input_filename = os.path.basename(input_path)
            output_filename = os.path.splitext(input_filename)[0] + '.mp3'
            output_path = os.path.join(output_folder, output_filename)
            
            # Load audio with pydub
            try:
                # Try loading as WAV first
                audio = AudioSegment.from_wav(input_path)
            except CouldntDecodeError:
                try:
                    # Try other formats
                    audio = AudioSegment.from_file(input_path)
                except CouldntDecodeError as e:
                    # Load with librosa and convert
                    y, sr = librosa.load(input_path, sr=None)
                    
                    # Convert to WAV first
                    temp_wav = os.path.join(TEMP_FOLDER, 'temp_export.wav')
                    sf.write(temp_wav, y, sr)
                    audio = AudioSegment.from_wav(temp_wav)
            
            # Export as MP3
            audio.export(
                output_path,
                format='mp3',
                bitrate=bitrate,
                codec='libmp3lame'
            )
            
            logger.info(f"MP3 export complete: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error exporting MP3: {str(e)}")
            raise

    def batch_export_mp3(self, input_paths, output_folder=OUTPUT_FOLDER):
        """Export multiple files as MP3"""
        results = []
        for input_path in input_paths:
            try:
                output_path = self.export_mp3(input_path, output_folder)
                results.append({
                    'input': input_path,
                    'output': output_path,
                    'success': True
                })
            except Exception as e:
                logger.error(f"Batch export failed for {input_path}: {str(e)}")
                results.append({
                    'input': input_path,
                    'error': str(e),
                    'success': False
                })
        
        return results
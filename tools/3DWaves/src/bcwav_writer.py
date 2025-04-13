import wave
import struct

def convert_to_bcwav(wav_path, output_path):
    with wave.open(wav_path, 'rb') as wav:
        nchannels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        framerate = wav.getframerate()
        nframes = wav.getnframes()
        audio_data = wav.readframes(nframes)

        if sampwidth != 2:
            raise ValueError("Only 16-bit PCM WAV files are supported.")

    with open(output_path, 'wb') as out:
        out.write(b'CWAV')
        out.write(struct.pack("<I", 0x00010000))  # Version
        out.write(struct.pack("<I", len(audio_data) + 0x20))  # Total size
        out.write(struct.pack("<I", nchannels))  # Channel count
        out.write(struct.pack("<I", framerate))  # Sample rate
        out.write(struct.pack("<I", sampwidth * 8))  # Bit depth
        out.write(struct.pack("<I", nframes))  # Number of frames
        out.write(b'\x00' * (0x20 - 28))  # Padding to reach 0x20
        out.write(audio_data)

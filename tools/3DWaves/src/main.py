import argparse
import os
import wave
import audioop
import tempfile
from bcwav_writer import convert_to_bcwav

def ensure_16bit_wav(input_path):
    with wave.open(input_path, 'rb') as wav:
        nchannels = wav.getnchannels()
        sampwidth = wav.getsampwidth()
        framerate = wav.getframerate()
        nframes = wav.getnframes()
        audio_data = wav.readframes(nframes)

    # If already 16-bit PCM, return original path
    if sampwidth == 2:
        return input_path

    # Convert to 16-bit PCM using audioop
    print("Converting to 16-bit PCM...")
    converted_data = audioop.lin2lin(audio_data, sampwidth, 2)

    # Write to temporary 16-bit WAV file
    tmp_path = tempfile.mktemp(suffix=".wav")
    with wave.open(tmp_path, 'wb') as out_wav:
        out_wav.setnchannels(nchannels)
        out_wav.setsampwidth(2)
        out_wav.setframerate(framerate)
        out_wav.writeframes(converted_data)

    return tmp_path

def main():
    parser = argparse.ArgumentParser(description="3DWaves - WAV to BCWAV Converter")
    parser.add_argument("input", help="Path to input WAV file")
    parser.add_argument("-o", "--output", help="Path to output BCWAV file")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or os.path.splitext(input_path)[0] + ".bcwav"

    if not os.path.exists(input_path):
        print(f"ERROR: Input file '{input_path}' not found.")
        return

    try:
        wav_16bit = ensure_16bit_wav(input_path)
        convert_to_bcwav(wav_16bit, output_path)
        print(f"Success! Output written to: {os.path.abspath(output_path)}")
        if wav_16bit != input_path:
            os.remove(wav_16bit)  # Clean up temp file
    except Exception as e:
        print(f"ERROR: Failed to convert file: {e}")

if __name__ == "__main__":
    main()

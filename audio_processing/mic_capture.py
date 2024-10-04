import pyaudio
import wave

def record_mic_audio(output_filename, record_seconds=10):
    chunk = 1024  # Record in chunks
    format = pyaudio.paInt16  # 16-bit resolution
    channels = 1  # Mono
    rate = 44100  # Sample rate in Hz
    p = pyaudio.PyAudio()

    # Open the stream
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []
    print("Recording Mic Audio...")

    # Record the audio in chunks
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a file
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

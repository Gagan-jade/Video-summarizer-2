import tkinter as tk
import pyaudio
import wave
import threading

# Global variable to control recording state
is_recording = False

def record_mic_audio(output_filename):
    global is_recording
    
    chunk = 1024  # Record in chunks
    format = pyaudio.paInt16  # 16-bit resolution
    channels = 1  # Mono
    rate = 44100  # Sample rate in Hz
    p = pyaudio.PyAudio()

    # Open the stream
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    frames = []
    print("Recording Mic Audio...")

    # Record the audio in chunks until is_recording is False
    while is_recording:
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

def start_recording():
    global is_recording
    is_recording = True  # Set the flag to start recording
    output_filename = 'mic_output.wav'  # Specify the output filename
    
    # Start recording in a new thread
    threading.Thread(target=record_mic_audio, args=(output_filename,)).start()

def stop_recording():
    global is_recording
    is_recording = False  # Set the flag to stop recording

# Initialize GUI
root = tk.Tk()
root.title("Audio Recorder")

# Start button
start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack()

# Stop button
stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack()

root.mainloop()

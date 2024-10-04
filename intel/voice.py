# import tkinter as tk
# import pyaudio
# import wave
# import threading

# # Global variable to control recording state
# is_recording = False

# def record_mic_audio(output_filename):
#     global is_recording
    
#     chunk = 1024  # Record in chunks
#     format = pyaudio.paInt16  # 16-bit resolution
#     channels = 1  # Mono
#     rate = 44100  # Sample rate in Hz
#     p = pyaudio.PyAudio()

#     # Open the stream
#     stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

#     frames = []
#     print("Recording Mic Audio...")

#     # Record the audio in chunks until is_recording is False
#     while is_recording:
#         data = stream.read(chunk)
#         frames.append(data)

#     print("Recording complete")

#     # Stop and close the stream
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     # Save the recorded audio to a file
#     wf = wave.open(output_filename, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(p.get_sample_size(format))
#     wf.setframerate(rate)
#     wf.writeframes(b''.join(frames))
#     wf.close()

# def start_recording():
#     global is_recording
#     is_recording = True  # Set the flag to start recording
#     output_filename = 'mic_output.wav'  # Specify the output filename
    
#     # Start recording in a new thread
#     threading.Thread(target=record_mic_audio, args=(output_filename,)).start()

# def stop_recording():
#     global is_recording
#     is_recording = False  # Set the flag to stop recording

# # Initialize GUI
# root = tk.Tk()
# root.title("Audio Recorder")

# # Start button
# start_button = tk.Button(root, text="Start Recording", command=start_recording)
# start_button.pack()

# # Stop button
# stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
# stop_button.pack()

# root.mainloop()














import tkinter as tk
import pyaudio
import wave
import threading
import subprocess
import os

# Global variable to control recording state
is_recording = False
ffmpeg_process = None  # To track the system audio recording process

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

def start_mic_recording():
    global is_recording
    is_recording = True  # Set the flag to start recording
    output_filename = 'mic_output.wav'  # Specify the output filename
    
    # Start microphone recording in a new thread
    threading.Thread(target=record_mic_audio, args=(output_filename,)).start()

def stop_mic_recording():
    global is_recording
    is_recording = False  # Set the flag to stop recording

# Function to start system audio recording using FFmpeg
def start_system_audio_recording():
    global ffmpeg_process
    output_filename = 'system_audio_output.wav'  # Output file for system audio
    command = [
        'ffmpeg',
        '-f', 'dshow',
        '-i', 'audio=Voicemeeter Out B1 (VB-Audio Voicemeeter VAIO)',
        output_filename
    ]
    
    print("Starting system audio recording...")
    
    # Start the FFmpeg process and store it in the ffmpeg_process variable
    ffmpeg_process = subprocess.Popen(command)
    
# Function to stop system audio recording
def stop_system_audio_recording():
    global ffmpeg_process
    if ffmpeg_process:
        print("Stopping system audio recording...")
        
        # Send a termination signal to FFmpeg process
        ffmpeg_process.terminate()
        ffmpeg_process.wait()  # Wait for the process to finish
        ffmpeg_process = None
        print("System audio recording stopped and saved.")

# Initialize GUI
root = tk.Tk()
root.title("Audio Recorder")

# Start mic recording button
start_mic_button = tk.Button(root, text="Start Mic Recording", command=start_mic_recording)
start_mic_button.pack()

# Stop mic recording button
stop_mic_button = tk.Button(root, text="Stop Mic Recording", command=stop_mic_recording)
stop_mic_button.pack()

# Start system audio recording button
start_sys_audio_button = tk.Button(root, text="Start System Audio", command=start_system_audio_recording)
start_sys_audio_button.pack()

# Stop system audio recording button
stop_sys_audio_button = tk.Button(root, text="Stop System Audio", command=stop_system_audio_recording)
stop_sys_audio_button.pack()

root.mainloop()

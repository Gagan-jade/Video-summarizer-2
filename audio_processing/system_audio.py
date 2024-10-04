from soundcard import get_microphone
# import soundcard as sc

# for mic in sc.all_microphones():
#     print(f"{mic.id}: {mic.name}")


def record_system_audio(output_filename, record_seconds=10):
    # Get the default microphone; specify None to get the default
    mic = get_microphone(None)  
    
    print("Recording system audio...")
    audio_data = mic.record(samplerate=44100, numframes=record_seconds * 44100)
    
    # Save the recorded audio data to a file
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)  # Set number of channels
        wf.setsampwidth(2)  # Set sample width (2 bytes for PCM)
        wf.setframerate(44100)  # Set sample rate
        wf.writeframes(audio_data)

    print("Recording complete.")

import soundcard as sc

def record_system_audio(output_filename, record_seconds=10):
    default_speaker = sc.default_speaker()
    audio_data = default_speaker.record(samplerate=44100, numframes=record_seconds * 44100)
    sc.write(output_filename, audio_data, samplerate=44100)
    print("System audio recorded")

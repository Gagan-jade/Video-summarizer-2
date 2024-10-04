import tkinter as tk
from audio_processing.mic_capture import record_mic_audio
from audio_processing.system_audio import record_system_audio
from audio_processing.transcription import transcribe_audio
from summarization.summarize import summarize_text

def start_recording():
    mic_output = "mic_output.wav"
    system_output = "system_output.wav"

    # Record mic and system audio
    record_mic_audio(mic_output)
    record_system_audio(system_output)

    # Transcribe both audios
    mic_transcript = transcribe_audio(mic_output)
    system_transcript = transcribe_audio(system_output)

    # Combine and summarize
    combined_text = mic_transcript + " " + system_transcript
    summary = summarize_text(combined_text)

    # Display summary in GUI
    summary_label.config(text=summary)

# Initialize GUI
root = tk.Tk()
root.title("Audio Summarizer")

# Start button
start_button = tk.Button(root, text="Start", command=start_recording)
start_button.pack()

# Summary output
summary_label = tk.Label(root, text="Summary will appear here.")
summary_label.pack()

root.mainloop()

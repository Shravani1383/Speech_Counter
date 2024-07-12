import random
from pydub import AudioSegment

# Function to split audio at random times
def split_audio_randomly(input_file, num_splits):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    duration = len(audio)  # Duration in milliseconds

    # Generate random split points
    split_points = sorted(random.sample(range(1, duration), num_splits - 1))
    split_points = [0] + split_points + [duration]

    # Split and export the audio
    for i in range(len(split_points) - 1):
        start_time = split_points[i]
        end_time = split_points[i + 1]
        chunk = audio[start_time:end_time]
        chunk.export(f"audio/output_chunk_{i + 1}.mp3", format="mp3")

    print(f"Audio split into {num_splits} chunks.")

# Example usage
split_audio_randomly("Audio.mp3", 7)  # Split into 5 random chunks

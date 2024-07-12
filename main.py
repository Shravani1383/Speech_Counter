import os
from pydub import AudioSegment

def check_audio_duration(folder_path, limit_minutes=5):
    limit_seconds = limit_minutes * 60
    total_duration = 0
    audio_files_info = []
    limit_reached_file = None
    limit_reached_duration = 0

    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.mp3', '.wav', '.ogg', '.flac')):
            audio_file_path = os.path.join(folder_path, file_name)
            try:
                audio = AudioSegment.from_file(audio_file_path)
                duration_seconds = len(audio) / 1000
                print(f"Processing file: {file_name}, Duration: {duration_seconds:.2f} seconds")  # Debugging statement

                if total_duration + duration_seconds >= limit_seconds:
                    limit_reached_file = file_name
                    limit_reached_duration = limit_seconds - total_duration
                    total_duration = limit_seconds
                    break
                else:
                    total_duration += duration_seconds
                    audio_files_info.append((file_name, duration_seconds))

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    if total_duration >= limit_seconds:
        notification = "You have reached your limit."
    else:
        notification = "Total duration is less than the limit."

    if limit_reached_file:
        audio_files_info.append((limit_reached_file, limit_reached_duration))

    return notification, audio_files_info, limit_reached_file, limit_reached_duration

# Example usage:
folder_path = 'audio'
notification, audio_files_info, limit_reached_file, limit_reached_duration = check_audio_duration(folder_path)

print(notification)
for file_name, duration in audio_files_info:
    print(f"File: {file_name}, Duration: {duration:.2f} seconds")
if limit_reached_file:
    print(f"Stopped accepting at file: {limit_reached_file}, Duration: {limit_reached_duration:.2f} seconds")

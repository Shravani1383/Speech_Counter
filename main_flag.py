import os
from pydub import AudioSegment

def check_audio_duration(folder_path, limit_minutes=5):
    limit_seconds = limit_minutes * 60
    alert_threshold_seconds = 3 * 60  # 3 minutes in seconds
    total_duration = 0
    time_consumed_before_alert = 0  # Variable to store time consumed before 3 min alert
    audio_files_info = []
    limit_reached_file = None
    limit_reached_duration = 0
    alert_triggered = False

    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.mp3', '.wav', '.ogg', '.flac')):
            audio_file_path = os.path.join(folder_path, file_name)
            try:
                audio = AudioSegment.from_file(audio_file_path)
                duration_seconds = len(audio) / 1000
                print(f"Processing file: {file_name}, Duration: {duration_seconds:.2f} seconds, Total Duration: {total_duration:.2f} seconds")  # Debugging statement

                if not alert_triggered and (total_duration + duration_seconds >= limit_seconds - alert_threshold_seconds):
                    time_consumed_before_alert = limit_seconds- alert_threshold_seconds # Store time consumed before alert
                    print(f"Alert: Last 3 minutes left! Consumed time: {time_consumed_before_alert}seconds")
                    alert_triggered = True

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

    return notification, audio_files_info, limit_reached_file, limit_reached_duration, time_consumed_before_alert

# Example usage:
folder_path = 'audio'
notification, audio_files_info, limit_reached_file, limit_reached_duration, time_consumed_before_alert = check_audio_duration(folder_path)

print(notification)
if limit_reached_file:
    print(f"Stopped accepting at file: {limit_reached_file}, Duration: {limit_reached_duration:.2f} seconds")

# print(f"Time consumed before 3 min alert: {time_consumed_before_alert:.2f} seconds")

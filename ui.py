import os
from pydub import AudioSegment
import streamlit as st
import tempfile

def check_audio_duration(files, limit_minutes=5):
    limit_seconds = limit_minutes * 60
    alert_threshold_seconds = 3 * 60  # 3 minutes in seconds
    total_duration = 0
    time_consumed_before_alert = 0  # Variable to store time consumed before 3 min alert
    audio_files_info = []
    limit_reached_file = None
    limit_reached_duration = 0
    alert_triggered = False

    for file in files:
        try:
            # Save the uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            audio = AudioSegment.from_file(temp_file_path)
            duration_seconds = len(audio) / 1000
            st.write(f"Processing file: {file.name}, Duration: {duration_seconds:.2f} seconds, Total Duration: {total_duration:.2f} seconds")  # Debugging statement

            if not alert_triggered and (total_duration + duration_seconds >= limit_seconds - alert_threshold_seconds):
                time_consumed_before_alert = limit_seconds - alert_threshold_seconds  # Store time consumed before alert
                st.write(f"Alert: Last 3 minutes left! Consumed time: {time_consumed_before_alert} seconds")
                alert_triggered = True

            if total_duration + duration_seconds >= limit_seconds:
                limit_reached_file = file.name
                limit_reached_duration = limit_seconds - total_duration
                total_duration = limit_seconds
                break
            else:
                total_duration += duration_seconds
                audio_files_info.append((file.name, duration_seconds))

        except Exception as e:
            st.write(f"Error processing file {file.name}: {e}")

    if total_duration >= limit_seconds:
        notification = "You have reached your limit."
    else:
        notification = "Total duration is less than the limit."

    if limit_reached_file:
        audio_files_info.append((limit_reached_file, limit_reached_duration))

    return notification, audio_files_info, limit_reached_file, limit_reached_duration, time_consumed_before_alert

# Streamlit UI
st.title("Audio Duration Checker")

uploaded_files = st.file_uploader("Upload one or more audio files", type=['mp3', 'wav', 'ogg', 'flac'], accept_multiple_files=True)

if st.button("Check Duration"):
    if uploaded_files:
        notification, audio_files_info, limit_reached_file, limit_reached_duration, time_consumed_before_alert = check_audio_duration(uploaded_files)
        st.write(notification)
        if limit_reached_file:
            st.write(f"Stopped accepting at file: {limit_reached_file}, Duration: {limit_reached_duration:.2f} seconds")
        st.write(f"Time consumed before 3 min alert: {time_consumed_before_alert:.2f} seconds")
        st.write("Audio Files Information:")
        for info in audio_files_info:
            st.write(f"File: {info[0]}, Duration: {info[1]:.2f} seconds")
    else:
        st.write("Please upload at least one audio file.")

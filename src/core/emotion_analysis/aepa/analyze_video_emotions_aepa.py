import os
import re
from pprint import pprint

import pandas as pd

from config.constants import DATASET_DIR, emotions_au
from core.emotion_analysis.visualization import generate_AEPA_plot


def list_all_files_in_directory(directory_path):
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                all_files.append(os.path.join(root, file))
    return all_files


def break_string(s):
    pattern = (
        r"^"
        r"(?P<type>full-AV-speech|audio-only-speech)"
        r"-"
        r"(?P<emotion>\w+)"
        r"-"
        r"(?P<intensity>\w+)"
        r"-"
        r"(?P<phrase>[\w-]+)"
        r"-"
        r"(?P<repetition>\d+[A-Za-z-]+)"
        r"-"
        r"(?P<actor>actor\d+)"
        r"(?:_animated)?"
        r"(?:\.csv)?"
        r"$"
    )
    m = re.match(pattern, s)
    return m.groupdict() if m else None


def analyze_video_emotions(video_path, threshold=2):
    df = pd.read_csv(video_path)
    filtered_df = df[[col for col in df.columns if col.startswith(" AU") and col.endswith("r")]]
    frame_emotions = {}
    emotion_counts = {emotion: 0 for emotion in emotions_au}
    dominant_frame = 0

    for idx, row in filtered_df.iterrows():
        emotion_sums = {emotion: 0 for emotion in emotions_au}
        for emotion, aus in emotions_au.items():
            for au in aus:
                col_name = f" AU{au:02}_r"
                if col_name in row and row[col_name] > threshold:
                    emotion_sums[emotion] += row[col_name]
        dominant_emotion = max(emotion_sums, key=emotion_sums.get)
        frame_emotions[idx] = dominant_emotion
        emotion_counts[dominant_emotion] += 1
        if emotion_sums[dominant_emotion] > emotion_sums.get(dominant_frame, 0):
            dominant_frame = idx

    dominant_frame_path = f"{video_path.replace('.csv', '')}_aligned/frame_det_00_{str(dominant_frame+1).zfill(6)}.bmp"
    video_name = os.path.basename(video_path)
    data = break_string(video_name)

    return {
        "emotion_counts": emotion_counts,
        "dominant_emotion_video": max(emotion_counts, key=emotion_counts.get),
        "dominant_frame": dominant_frame,
        "dominant_frame_path": dominant_frame_path,
        "video_name": video_name,
        "data": data,
    }


def main(directory=DATASET_DIR, threshold=0.7):
    video_files = list_all_files_in_directory(directory)

    for video in video_files:
        if video.endswith(".csv"):
            analysis_result = analyze_video_emotions(video, threshold=threshold)
            pprint(analysis_result)
            generate_AEPA_plot.generate_plot(analysis_result, "AEPA")


if __name__ == "__main__":
    main()

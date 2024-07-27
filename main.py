import json

import pandas as pd

import transform
from models import Session, YouTubeVideo
from program_api_connector import ProgramAPIConnector

SESSIONS_URL = "https://programapi24.europython.eu/2024/sessions.json"
SPEAKERS_URL = "https://programapi24.europython.eu/2024/speakers.json"
SESSION_TYPES_TO_INCLUDE = ("talk", "keynote", "sponsored", "panel")
EXCEPTIONS = ("Opening Session", "Closing Session")


def write_to_csv(sessions: list[YouTubeVideo], output_file: str):
    df = pd.DataFrame([json.loads(session.model_dump_json()) for session in sessions])
    df.to_csv(output_file, index=False)


def main(output_file: str = "youtube_videos.csv"):
    connector = ProgramAPIConnector()
    connector.fetch_data(SESSIONS_URL, SPEAKERS_URL)

    sessions: list[Session] = []
    for session in connector.sessions:
        if (
            not session.session_type.lower().startswith(SESSION_TYPES_TO_INCLUDE)
            and not session.title in EXCEPTIONS
        ):  # skip non-talks
            continue
        sessions.append(session)

    youtube_videos = [transform.session_to_youtube(session) for session in sessions]

    write_to_csv(youtube_videos, output_file)


if __name__ == "__main__":
    main()

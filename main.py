import json

import pandas as pd

import transform
from models import Session, VideoReviewSheetItem
from program_api_connector import ProgramAPIConnector
from sort import Sort

SESSIONS_URL = "https://programapi24.europython.eu/2024/sessions.json"
SPEAKERS_URL = "https://programapi24.europython.eu/2024/speakers.json"
SESSION_TYPES_TO_INCLUDE = ("talk", "keynote", "sponsored", "panel")
EXCEPTIONS = ("Opening Session", "Closing Session")
SORT_KEYS = ["date", "room", "start"]


def sort_and_write_to_csv(sessions: list[VideoReviewSheetItem], output_file: str):
    sessions_dumped = [
        json.loads(session.model_dump_json(by_alias=True)) for session in sessions
    ]
    sessions_sorted = Sort.sort_nested(sessions_dumped, SORT_KEYS)

    df = pd.DataFrame(sessions_sorted)
    df.to_csv(output_file, index=False)


def main(output_file: str = "video_review_sheet.csv"):
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

    video_review_sheet = [
        transform.session_to_video_review_sheet_item(session) for session in sessions
    ]

    sort_and_write_to_csv(video_review_sheet, output_file)


if __name__ == "__main__":
    main()

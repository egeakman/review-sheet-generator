from collections import defaultdict

import requests

from models import Session, Speaker


class ProgramAPIConnector:
    def __init__(self):
        self.sessions: set[Session] = set()
        self.sessions_by_code: dict[str, Session] = defaultdict(Session)

        self._speakers: set[Speaker] = set()
        self._speaker_names_by_code: dict[str, str] = defaultdict(str)

    def _fetch_url(self, url: str):
        response = requests.get(url)
        return response.json()

    def _parse_sessions(self, sessions_data: dict):
        sessions = set()
        for session_data in sessions_data.values():
            session = Session(
                code=session_data["code"],
                title=session_data["title"],
                speakers=[
                    self._speaker_names_by_code[speaker_code]
                    for speaker_code in session_data["speakers"]
                ],
                session_type=session_data["session_type"],
                track=session_data.get("track"),
                abstract=session_data.get("abstract", ""),
                website_url=session_data["website_url"],
                room=session_data["room"],
                start=session_data["start"],
            )
            sessions.add(session)
        return sessions

    def _parse_speakers(self, speakers_data: dict):
        speakers = set()
        for speaker_data in speakers_data.values():
            speaker = Speaker.model_validate(speaker_data)
            self._speaker_names_by_code[speaker.code] = speaker.name
            speakers.add(speaker)
        return speakers

    def fetch_data(self, sessions_url: str, speakers_url: str):
        speakers_data = self._fetch_url(speakers_url)
        sessions_data = self._fetch_url(sessions_url)

        self._speakers = self._parse_speakers(speakers_data)

        self.sessions = self._parse_sessions(sessions_data)
        self.sessions_by_code = {session.code: session for session in self.sessions}

    def get_session(self, code: str):
        return self.sessions_by_code.get(code)

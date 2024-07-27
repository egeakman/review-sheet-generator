from datetime import datetime

from models import Session, YouTubeVideo


def session_to_youtube(session: Session) -> YouTubeVideo:
    if session.speaker_names is None:
        title = f"EuroPython 2024 — {session.title}"
    else:
        title = f"{session.title} — {session.speaker_names}"

    description = f"""\
[EuroPython 2024 — {session.room} at {datetime.strftime(session.start, "%Y-%m-%d %H:%M")}]
{session.website_url}

{session.abstract}

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
http://creativecommons.org/licenses/by-nc-sa/4.0/
"""

    return YouTubeVideo(title=title, description=description)

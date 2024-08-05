from datetime import datetime

from models import Session, VideoReviewSheetItem


def session_to_video_review_sheet_item(session: Session) -> VideoReviewSheetItem:
    if session.speaker_names is None:
        youtube_title = f"EuroPython 2024 — {session.title}"
    else:
        title_with_speakers = f"{session.title} — {session.speaker_names}"

        # YouTube titles are limited to 100 characters,
        # so we omit the speaker names if the title is too long
        youtube_title = (
            title_with_speakers if len(title_with_speakers) <= 100 else session.title
        )

    youtube_description = f"""\
[EuroPython 2024 — {session.room} at {datetime.strftime(session.start, "%Y-%m-%d %H:%M")}]

{session.title} by {session.speaker_names}
{session.website_url}

{session.abstract}


---
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License: https://creativecommons.org/licenses/by-nc-sa/4.0/"""

    video_review_sheet_item = VideoReviewSheetItem(
        session_code=session.code,
        session_title=session.title,
        session_speaker_names=session.speaker_names,
        session_website_url=session.website_url,
        session_room=session.room,
        session_start=session.start,
        session_date=session.session_date,
        youtube_title=youtube_title,
        youtube_description=youtube_description,
        youtube_url=None,  # TODO: fill this in
    )

    return video_review_sheet_item

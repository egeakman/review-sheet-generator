from datetime import datetime

from pydantic import BaseModel, Field, computed_field


class Speaker(BaseModel):
    code: str
    name: str

    def __hash__(self):
        return hash(self.code)


class Session(BaseModel):
    code: str
    title: str
    speakers: list[str] = Field(..., exclude=True)
    session_type: str = Field(..., exclude=True)
    track: str | None
    abstract: str = ""
    website_url: str
    room: str
    start: datetime

    @computed_field
    def speaker_names(self) -> str | None:
        return ", ".join(self.speakers) or None

    def __hash__(self):
        return hash(self.code)


class VideoReviewSheetItem(BaseModel):
    session_code: str = Field(..., serialization_alias="Code")
    session_title: str = Field(..., serialization_alias="Title")
    session_speaker_names: str | None = Field(..., serialization_alias="Speaker Names")
    session_website_url: str = Field(..., serialization_alias="Website URL")
    youtube_title: str = Field(..., serialization_alias="YouTube Title")
    youtube_description: str = Field(..., serialization_alias="YouTube Description")
    session_room: str = Field(..., serialization_alias="room")
    session_start: datetime = Field(..., serialization_alias="start") 
    youtube_url: str | None = Field(None, serialization_alias="YouTube URL")

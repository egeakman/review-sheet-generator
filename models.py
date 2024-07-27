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


class YouTubeVideo(BaseModel):
    title: str
    description: str

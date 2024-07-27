import pytest

import main
import transform
from models import Session
from program_api_connector import ProgramAPIConnector


@pytest.fixture
def mock_connector(mocker):
    connector = mocker.Mock(spec=ProgramAPIConnector)
    connector.sessions = [
        Session(
            session_type="talk",
            title="Sample Talk",
            code="T01",
            speakers=["Speaker 1"],
            track="Track 1",
            website_url="http://example.com/talk1",
            room="Room 1",
            start="2024-07-27T10:00:00Z",
            other_field="value",
        ),
        Session(
            session_type="keynote",
            title="Sample Keynote",
            code="K01",
            speakers=["Speaker 2"],
            track="Track 2",
            website_url="http://example.com/keynote1",
            room="Room 2",
            start="2024-07-27T11:00:00Z",
            other_field="value",
        ),
        Session(
            session_type="workshop",
            title="Sample Workshop",
            code="W01",
            speakers=["Speaker 3"],
            track="Track 3",
            website_url="http://example.com/workshop1",
            room="Room 3",
            start="2024-07-27T12:00:00Z",
            other_field="value",
        ),
        Session(
            session_type="talk",
            title="Opening Session",
            code="O01",
            speakers=["Speaker 4"],
            track="Track 4",
            website_url="http://example.com/opening",
            room="Room 4",
            start="2024-07-27T09:00:00Z",
            other_field="value",
        ),
        Session(
            session_type="panel",
            title="Sample Panel",
            code="P01",
            speakers=["Speaker 5"],
            track="Track 5",
            website_url="http://example.com/panel1",
            room="Room 5",
            start="2024-07-27T13:00:00Z",
            other_field="value",
        ),
    ]
    mocker.patch("main.ProgramAPIConnector", return_value=connector)
    return connector


def test_main(mock_connector, tmp_path, mocker):
    mock_write_to_csv = mocker.patch("main.write_to_csv")
    output_file = tmp_path / "youtube_videos.csv"

    main.main(output_file=str(output_file))

    expected_sessions = [
        mock_connector.sessions[0],  # Sample Talk
        mock_connector.sessions[1],  # Sample Keynote
        mock_connector.sessions[3],  # Opening Session (since it should be included)
        mock_connector.sessions[4],  # Sample Panel
    ]
    youtube_videos = [
        transform.session_to_youtube(session) for session in expected_sessions
    ]

    mock_write_to_csv.assert_called_once_with(youtube_videos, str(output_file))

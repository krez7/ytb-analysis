from typing import TYPE_CHECKING
from urllib.error import HTTPError

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

type JsonType = dict[str, JsonType] | dict[str, str] | dict[str, int]

class ChannelInstance:

    _channel_id: str
    _uploads_id: str
    _service: Resource
    _videos_list: list[JsonType]

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def uploads_id(self):
        if self._uploads_id == "":
            playlistId_request = self._service.channels().list(part="contentDetails", id = self.channel_id)
            try:
                self._uploads_id = playlistId_request.execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            except HTTPError as e:
                print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return self._uploads_id

    def _list_videos(self, segmentation: int):

        playlistItems_request = self._service.playlistItems().list(part="snippet", playlistId = self.uploads_id, maxResults=segmentation)
        try:
            while (playlistItems_request is not None):
                playlistItems_resources = playlistItems_request.execute()
                yield playlistItems_resources
                playlistItems_request = self._service.playlistItems().list_next(playlistItems_request, playlistItems_resources)

        except HTTPError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))       

    @property
    def videos_list(self):
        if not self._videos_list:
            for res in self._list_videos(50):
                self._videos_list += res.get("items")
        return self._videos_list

    def __init__(self, service: Resource, channel_id: str):
        self._channel_id = channel_id
        self._uploads_id = ""
        self._service = service
        self._videos_list = []

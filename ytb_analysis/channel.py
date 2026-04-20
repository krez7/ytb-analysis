from typing import TYPE_CHECKING
from urllib.error import HTTPError

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource


class ChannelInstance:

    _channel_id: str
    _service: Resource
    _videos_list: list[str]

    @property
    def channel_id(self):
        if self._channel_id is None:
            channel_request = self._service.channels().list(part="contentDetails.relatedPlaylists.uploads",
                                                            id=self._channel_id)
            channel_resources: Resource = None
            try:
                channel_resources = channel_request.execute()

            except HTTPError as e:
                print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

            self._channel_id = channel_resources.items.id

        return self._channel_id

    def _list_videos(self, segmentation: int):
            
        playlistItems_request = self._service.playlistItems().list(part="snippet", playlistId = self.channel_id[0] + "U" + self.channel_id[2:], maxResults=segmentation)
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
        self._service = service
        self._videos_list = []

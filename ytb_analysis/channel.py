from typing import TYPE_CHECKING
from urllib.error import HTTPError

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

type JsonType = dict[str, list[JsonType] | JsonType | str | bool | float | int | None]

class ChannelInstance:

    _channel_id: str
    _service: Resource
    _channel_informations: JsonType
    _videos_list: list[JsonType]
    _videos_stats: list[JsonType]

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def channel_informations(self):
        if self._channel_informations == {}:
            information_request = self._service.channels().list(part="contentDetails,statistics", id = self.channel_id)
            try:
                self._channel_informations = information_request.execute().get("items")[0]
            except HTTPError as e:
                print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return self._channel_informations

    def _list_videos(self, segmentation: int):

        playlistItems_request = self._service.playlistItems().list(part="snippet", playlistId = self.channel_informations["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=segmentation)
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

    @property
    def videos_stats(self):
        if not self._videos_stats:
            id: str = ""
            for video in self.videos_list:
                id += video["snippet"]["resourceId"]["videoId"]  + ","
            id = id[:-1]
            batchStats_request = self._service.videos().batchGetStats(id=id, part="contentDetails, id, snippet, statistics")
            try:
                self._videos_stats = batchStats_request.execute().get("items")
            except HTTPError as e:
                print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))
        return self._videos_stats

    def __init__(self, service: Resource, channel_id: str):
        self._channel_id = channel_id
        self._service = service
        self._channel_informations = {}
        self._videos_list = []
        self._videos_stats = []

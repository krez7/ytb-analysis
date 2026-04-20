import pytest

import json
from googleapiclient.discovery import build
from googleapiclient.http import HttpMockSequence

from ytb_analysis.channel import ChannelInstance


class TestChannelInstance:

    def test_videos_list(self):
        examples = []
        for i in range(4):
            examples.append(({"status": "200"},json.dumps(json.load(open("responses/videos_list_" + str(i) + ".json")))))
            
        http = HttpMockSequence(examples) 
        service = build("youtube", "v3", http=http)
        instance = ChannelInstance(service, "test")
        assert instance.videos_list == json.load(open("responses/expected_videos_list.json")).get("items")

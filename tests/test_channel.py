import pytest

import json
from googleapiclient.discovery import build
from googleapiclient.http import HttpMockSequence
from pathlib import Path

from ytb_analysis.channel import ChannelInstance

curr_dir = str(Path(__file__).parent)

class TestChannelInstance:

    @pytest.fixture
    def instance(self):
        examples = []

        for i in range(4):
            examples.append(({"status": "200"},json.dumps(json.load(open(curr_dir + "/responses/videos_list_" + str(i) + ".json")))))

        http = HttpMockSequence(examples)
        service = build("youtube", "v3", http=http)
        return ChannelInstance(service, "test")

    def test_videos_list(self, instance):
        assert instance.videos_list == json.load(open(curr_dir + "/responses/expected_videos_list.json")).get("items")

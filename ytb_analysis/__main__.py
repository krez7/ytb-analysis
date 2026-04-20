from googleapiclient.discovery import build

from .channel import ChannelInstance

if __name__ == "__main__":
    
    api_key = input("Enter your Youtube Data API key : ")
    channel_id = input("Enter the channel's ID : ")

    service = build("youtube", "v3", developerKey=api_key)
    
    instance = ChannelInstance(service, channel_id)

    print(instance.videos_list)

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from .channel import ChannelInstance

if __name__ == "__main__":

    api_key = ""
    oauth_credentials = None

    answer = input("Do you wish to provide OAuth access ? (y/n) : ")

    if answer == "y":
        oauth_secret_file = input("Enter your OAuth credientals file's name (must be in the root directory of the project) : ")
        flow = InstalledAppFlow.from_client_secrets_file(oauth_secret_file, ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/yt-analytics.readonly"])
        oauth_credentials = flow.run_local_server()
    else:
        api_key = input("Enter your Youtube Data API key : ")

    channel_id = input("Enter the channel's ID : ")

    service = build("youtube", "v3", developerKey=api_key, credentials = oauth_credentials)
    
    instance = ChannelInstance(service, channel_id)

    print(instance.channel_informations)
    print(instance.videos_stats)

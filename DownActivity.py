from flet import Row, Image, Column, Text
from pytube import YouTube, Stream

class DownActivity:
    def __init__(self, _video: YouTube, _stream: Stream, _url: str = ""):
        self.video = _video,
        self.stream = _stream,
        self.url = _url

    def ShowActivity(self) -> Row:
        return Row([
                Image(self.video.thumbnail_url, width=240),
                Column(controls=[
                    Text(self.video.title, size=30),
                ])
            ])
    
    def getURL(self) -> str:
        return self.url

    def getStream(self) -> Stream:
        return self.stream
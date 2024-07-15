from flet import Row, Image, Column, Text, ProgressBar
from pytube import YouTube, Stream

class DownActivity:
    def __init__(self, _yt: YouTube, _stream: Stream, _path: str = ""):
        self.stream = _stream,
        self.path = _path
        self.yt = _yt

        self.progress_bar = ProgressBar(value=0,width=400)
        self.progress_label = Text("0%")

    def showActivity(self) -> Row:
        return Row(controls=[
                Image(video.thumbnail_url, width=240),
                Column(controls=[
                    Text(video.title, size=30),
                    Row([
                        self.progress_bar,
                        self.progress_label
                    ])
                ])
            ])

    def getPath(self) -> str:
        return self.path

    def getStream(self) -> Stream:
        return self.stream[0]
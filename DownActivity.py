from flet import Row, Image, Column, Text
from pytube import YouTube, Stream

class DownActivity:
    def __init__(self, _stream: Stream, _path: str = ""):
        self.stream = _stream,
        self.path = _path

    def getPath(self) -> str:
        return self.path

    def getStream(self) -> Stream:
        return self.stream[0]
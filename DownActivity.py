from flet import Row, Image, Column, Text, ProgressBar
from pytubefix import YouTube, Stream


class DownActivity:
    def __init__(self, _yt: YouTube, _stream: Stream, _path: str = ""):
        self.stream = _stream,
        self.path = _path
        self.yt = _yt

        self.progress_bar = ProgressBar(value=0, width=400)
        self.progress_label = Text("0%")

    def show_activity(self) -> Row:
        return Row(controls=[
            Image(self.yt.thumbnail_url, width=240),
            Column(controls=[
                Text(self.yt.title, size=30),
                Row([
                    self.progress_bar,
                    self.progress_label
                ])
            ])
        ])

    def set_progress(self, progress: int):
        self.progress_bar.value = progress / 100
        self.progress_label.value = f"{progress}%"

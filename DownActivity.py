import flet as ft
import os
from pytube import Stream, YouTube

class DownActivity():
    def __init__(self, _yt: YouTube):
        self.yt = _yt
        # self.yt.register_on_progress_callback(on_progress)
        self.progress_bar = ft.ProgressBar(width=400, value=0)
        self.progress_label = ft.Text("0%")

    def ShowActivity(self) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                        ft.Image(self.yt.thumbnail_url, width=240),
                        ft.Column([
                            ft.Text(self.yt.title, size=30),
                            ft.Row([
                                self.progress_bar,
                                self.progress_label
                            ]),
                        ])
                ])
            )
        )

    def setProgress(self, new_progress: float):
        progress = round(new_progress)

        self.progress_label.value = f"{progress}%"
        self.progress_bar.value = progress / 100

        print(porcent)

        self.update()

    def on_progress(self, stream: Stream, chunk, bytes_remaining):
        print("hello")
        total_size = stream.filesize
        bytes_down = total_size - bytes_remaining
        porcent = round(bytes_down / total_size * 100)

        self.setProgress(porcent)

    def DownloadVideo(self, stream: Stream, path: str = ""):
        self.ShowActivity()

        if(path != ""):
            stream.download(output_path=path)
        else:
            stream.download(output_path=f"{os.path.expanduser('~')}\\Downloads")

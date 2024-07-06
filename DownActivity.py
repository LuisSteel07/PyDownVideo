import flet as ft
import os
from pytube import Stream, YouTube


class DownActivity():
    def __init__(self, url: str):
        self.yt = YouTube(url, on_progress_callback=self.on_progress)

        self.progress_bar = ft.ProgressBar(width=400, value=0)
        self.progress_label = ft.Text("0%")

    def ShowActivity(self) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                        ft.Image(self.yt.thumbnail_url, width=240),
                        ft.Text(self.yt.title, size=30),
                        ft.Row([
                            self.progress_bar,
                            self.progress_label
                        ])
                ])
            )
        )

    def setProgress(self, new_progress: float):
        progress = round(new_progress, 2)

        self.progress_label.value = f"{progress}%"
        self.progress_bar.value = progress / 100

        print(porcent)

    def on_progress(stream: Stream, chunk, bytes_remaining):
        # total_size = stream.filesize
        # bytes_down = total_size - bytes_remaining
        # porcent = bytes_down / total_size * 100

        # self.setProgress()

        print("funciono")


    def DownloadVideo(self, stream: Stream, path: str = ""):
        self.ShowActivity()

        if(path != ""):
            stream.download(output_path=path)
        elif(textfield_PATH_FILE.value == ""):
            stream.download(output_path=f"{os.path.expanduser('~')}\\Downloads")


    


import flet as ft
from pytube import Stream, YouTube

class DownActivity():
    def __init__(self, _yt: YouTube):
        self.yt = _yt
        
        self.filesize_mb = self.yt.streams.get_lowest_resolution().filesize_mb


    def ShowActivity(self) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(self.yt.thumbnail_url, width=240),
                        ft.Column([
                            ft.Text(self.yt.title, size=30),
                            ft.Text(f"{self.filesize_mb} MB")
                        ]),
                    ]
                )
            )
        )
import flet as ft
from pytube import Stream, YouTube

class DownActivity():
    def __init__(self, _yt: YouTube):
        self.yt = _yt

    def ShowActivity(self) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(self.yt.thumbnail_url, width=240),
                        ft.Text(self.yt.title, size=30),
                    ]
                )
            )
        )
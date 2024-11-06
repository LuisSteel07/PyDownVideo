import flet as ft
from pytubefix import YouTube

from util import wrap_text


class SelectVideo:
    def __init__(self, title: str, photo: str, video: YouTube):
        self.title = title
        self.photo = photo
        self.video = video
        self.checkbox = ft.Checkbox(value=True)

    def show_select_video(self):
        return ft.Row(
            controls=[
                self.checkbox,
                ft.Image(self.photo, width=240),
                ft.Text(wrap_text(self.title), size=25)
            ]
        )

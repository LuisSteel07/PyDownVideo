import flet as ft
from pytubefix import YouTube
from util import wrap_text


class SelectVideo:
    def __init__(self, title: str, photo: str, video: YouTube):
        self.title = title
        self.photo = photo
        self.video = video
        self.checkbox = ft.Checkbox(value=True)
        self.container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(self.photo, width=300),
                    ft.Text(
                        wrap_text(self.title, limit=25),
                        size=18,
                        weight=ft.FontWeight.BOLD,

                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=400
            ),
            bgcolor=ft.colors.INDIGO_900,
            width=300,
            height=300,
            border_radius=20,
            blur=0,
            animate=ft.animation.Animation(150, ft.AnimationCurve.LINEAR),
            on_click=self.on_click_event
        )

    def on_click_event(self, e):
        self.checkbox.value = not self.checkbox.value

        self.container.width = 250 if self.container.width == 300 else 300
        self.container.height = 250 if self.container.height == 300 else 300
        self.container.blur = 10 if self.container.blur == 0 else 0
        self.container.bgcolor = ft.colors.GREY_900 if self.container.bgcolor == ft.colors.INDIGO_900 else ft.colors.INDIGO_900
        self.container.update()

    def show_select_video(self):
        return self.container

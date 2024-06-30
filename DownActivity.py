import flet as ft

class DownActivity():
    def __init__(self, _title, _thumbnail):
        self.title = _title,
        self.thumbnail = _thumbnail

    def ShowActivity(self) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Image(self.getThumbnail(), width=240),
                        ft.Column(
                            [
                                ft.Text(self.getTitle(), size=30),
                                ft.ProgressBar(width=400)
                            ]
                        )
                    ]
                )
            )
        )

    def getTitle(self) -> str:
        return self.title

    def getThumbnail(self) -> str:
        return self.thumbnail
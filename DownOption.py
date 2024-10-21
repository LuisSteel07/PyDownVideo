from pytubefix import Stream, YouTube
import flet as ft


class DownOption:
    def __init__(self, _stream: Stream):
        self.stream = _stream

    def show_option(self, function_down) -> ft.DataRow:
        if self.stream.type == "video":
            return ft.DataRow([
                ft.DataCell(ft.Text("Video")),
                ft.DataCell(ft.Text(self.stream.resolution)),
                ft.DataCell(ft.Text(f"{self.stream.filesize_mb} mb")),
                ft.DataCell(ft.Text(self.stream.mime_type)),
                ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: function_down(
                    self.stream))),
            ])
        elif self.stream.type == "audio":
            return ft.DataRow([
                ft.DataCell(ft.Text("Audio")),
                ft.DataCell(ft.Text(self.stream.abr)),
                ft.DataCell(ft.Text(f"{self.stream.filesize_mb} mb")),
                ft.DataCell(ft.Text(self.stream.mime_type)),
                ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: function_down(
                    self.stream))),
            ])

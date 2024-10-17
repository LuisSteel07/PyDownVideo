from pytubefix import Stream
import flet as ft


class DownOption:
    def __init__(self, _stream: Stream):
        self.stream = _stream

    def show_option(self, function_down) -> ft.DataRow:
        if self.stream.type == "video":
            have_audio = ft.Text("Audio", color=ft.colors.GREEN)
            if not self.stream.is_progressive:
                have_audio = ft.Text("No Audio", color=ft.colors.RED)

            return ft.DataRow([
                ft.DataCell(ft.Text("Video")),
                ft.DataCell(ft.Text(self.stream.resolution)),
                ft.DataCell(ft.Text(f"{self.stream.filesize_mb} mb")),
                ft.DataCell(ft.Text(self.stream.mime_type)),
                ft.DataCell(have_audio),
                ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: function_down(
                    self.stream))),
            ])

        elif self.stream.type == "audio":
            return ft.DataRow([
                ft.DataCell(ft.Text("Audio")),
                ft.DataCell(ft.Text(self.stream.abr)),
                ft.DataCell(ft.Text(f"{self.stream.filesize_mb} mb")),
                ft.DataCell(ft.Text(self.stream.mime_type)),
                ft.DataCell(ft.Text("None", color=ft.colors.GREY)),
                ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: function_down(
                    self.stream))),
            ])

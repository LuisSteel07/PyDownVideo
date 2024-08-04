import flet as ft
from pytubefix import Playlist


def down_options_playlist(playlist: Playlist, page: ft.Page, list_options: ft.Row):
    list_options.controls.append(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Calidad")),
                ft.DataColumn(ft.Text("Acción"))
            ],
            rows=[
                ft.DataRow([
                    ft.DataCell(ft.Text("Video")),
                    ft.DataCell(ft.Text("Alto")),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD,
                                              on_click=lambda e: download_playlist(playlist, "higt"))),
                ]),
                ft.DataRow([
                    ft.DataCell(ft.Text("Video")),
                    ft.DataCell(ft.Text("Bajo")),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD,
                                              on_click=lambda e: download_playlist(playlist, "low"))),
                ]),
                ft.DataRow([
                    ft.DataCell(ft.Text("Audio")),
                    ft.DataCell(ft.Text("Alto")),
                    ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD,
                                              on_click=lambda e: download_playlist(playlist, "audio"))),
                ]),
            ]
        )
    )
    page.update()

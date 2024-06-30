import flet as ft
from pytube import YouTube, Stream
from DownActivity import DownActivity


def main(page: ft.Page):
    page.title = "PyDownVideo"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    title = ft.Text(value="PyDownVideo",size=30,weight=ft.FontWeight.BOLD)
    title1 = ft.Text(value="PyDownVideo",size=30,weight=ft.FontWeight.BOLD)

    def ShowAlert(e) -> ft.AlertDialog :

        yt = YouTube(textfield_URL.value)

        types = []

        for res in yt.streams:
            types.append(ft.dropdown.Option(res.resolution))

        type_archive = ft.Dropdown(
            label="Tipo de Archivo",
            options=[
                ft.dropdown.Option("Video"),
                ft.dropdown.Option("Audio")
            ]
        )

        type_list = ft.Dropdown(
            label="Resolusion",
            options=[
                types
            ]
        )


        return ft.AlertDialog(
            modal=True,
            title=ft.Text("Propiedades de Video & Audio"),
            content=[
                type_archive,
                type_list

            ],
            actions=[
                ft.TextButton("Aceptar"),
                ft.TextButton("Cerrar", on_click=lambda e: page.close_dialog()),
            ],
        )

    def Download(e):
        yt = YouTube(textfield_URL.value)
        
        listDownActivities.controls.append(DownActivity(yt.title, yt.thumbnail_url).ShowActivity())

        page.update()
        

    textfield_URL = ft.TextField(label="URL")
    dropdown_RESOLUTION = ft.Dropdown(
        label="Resolution", 
        options=[
            ft.dropdown.Option("1080p"),
            ft.dropdown.Option("480p"),
            ft.dropdown.Option("240p"),
            ft.dropdown.Option("144p"),
        ]    
    )

    listDownActivities = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        controls=[]
    )

    page.add(
            title,
            title1,
            ft.Column(controls=[
                textfield_URL,
                dropdown_RESOLUTION
            ]),
            ft.IconButton(icon=ft.icons.SEARCH, on_click=lambda e: page.show_dialog(ShowAlert(e))),
            listDownActivities
    )

ft.app(main)

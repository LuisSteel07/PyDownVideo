import flet as ft
import os
from pytube import YouTube, Stream
from DownActivity import DownActivity

def main(page: ft.Page):
    page.title = "PyDownVideo"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.DARK

    title = ft.Text(value="PyDownVideo",size=30,weight=ft.FontWeight.BOLD)

    progress = ft.ProgressBar(value=0, width=400)
    label_progress = ft.Text("0%")
    estado = ft.Text("",size=22, weight=ft.FontWeight.BOLD)
    textfield_PATH_FILE = ft.TextField(label="Directorio", width=600,tooltip="Coloque un directorio donde desea que se guarde el video/audio (Predeterminado es Download)")

    config_alert = ft.AlertDialog(
        modal=True,
        adaptive=True,
        title=ft.Text("Establecer Ruta de Descarga:"),
        content=textfield_PATH_FILE,
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(config_alert)),
        ],
    )

    listActivity = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[]
        )

    progressRing = ft.Row([
        ft.Column([
            ft.Row([
                ft.ProgressRing(),
            ],alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Buscando Archivo..."),
        ]),
    ], alignment=ft.MainAxisAlignment.CENTER)

    def on_progress(stream: Stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_down = total_size - bytes_remaining
        porcent = bytes_down / total_size * 100

        label_progress.value = f"{round(porcent,2)}%"
        progress.value = round(porcent,2) / 100

        if(round(porcent,2) == 100):
            label_progress.value = "0%"
            progress.value = 0
            listActivity.controls = []
            estado.value = "Archivo Descargado"
            estado.color = ft.colors.GREEN

            textfield_URL.disabled = False
            SearchButton.disabled = False

        page.update()

    def Validacion(e) :
        textfield_URL.color = "white"
        page.update()
        try:
            SearchButton.disabled = True
            textfield_URL.disabled = True
            page.add(progressRing)

            page.update()
            yt = YouTube(textfield_URL.value, on_progress_callback=on_progress)

            page.remove(progressRing)
            Download(yt)

            page.update()
        except Exception as err:
            textfield_URL.value = "URL Invalida"
            textfield_URL.color = ft.colors.RED
            print(err)
            SearchButton.disabled = False
            textfield_URL.disabled = False
            page.remove(progressRing)
            page.update()

    def Download(yt: YouTube):
        listActivity.controls.append(DownActivity(yt).ShowActivity())

        estado.value = "Descargando Archivo..."
        estado.color = ft.colors.BLUE
        textfield_PATH_FILE.color = ft.colors.WHITE

        page.update()

        try:

            if(textfield_PATH_FILE.value == ""):
                yt.streams.get_lowest_resolution().download(output_path=f"{os.path.expanduser('~')}\\Downloads")
            else:
                yt.streams.get_lowest_resolution().download(output_path=textfield_PATH_FILE.value)
        
        except Exception as err:
            textfield_PATH_FILE.value = "Directorio Invalido"
            textfield_PATH_FILE.color = ft.colors.RED
            print(err)
            page.update()

    SearchButton = ft.IconButton(icon=ft.icons.SEARCH, on_click=Validacion)
    textfield_URL = ft.TextField(label="URL", width=600)

    AppBar = ft.AppBar(
        title=title,
        leading=ft.Container(content=ft.Image("./src/source/python.svg",width=120),padding=20),
        leading_width = 100,
        center_title=False,
        toolbar_height=75,
        bgcolor=ft.colors.GREY_800,
        actions=[
            ft.Container(
                content=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Ruta de Descarga", on_click= lambda e: page.open(config_alert)),
                        ft.PopupMenuItem(text="Tema", on_click= lambda e: page.open(config_alert))
                    ]
                )
            )
        ]
    )

    page.appbar = AppBar

    page.add(
            ft.Row(
                controls=[
                    textfield_URL,
                    SearchButton,
                    estado
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[
                    progress,
                    label_progress
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ),
            listActivity
    )

ft.app(main)

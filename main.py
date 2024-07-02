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

    listActivity = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[]
        )

    listDownActivities = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )

    progressRing = ft.Column([
        ft.ProgressRing(),
        ft.Text("Buscando Archivo..."),
    ])

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

            listDownActivities.controls.append(DownActivity(yt).ShowActivity())

            OptionsDown(yt.streams)

            page.remove(progressRing)
            page.update()

        except Exception as err:
            textfield_URL.value = "URL Invalida"
            textfield_URL.color = ft.colors.RED
            print(err)
            SearchButton.disabled = False
            textfield_URL.disabled = False
            page.remove(progressRing)
            page.update()

    def OptionsDown(streams):
        listDownActivities.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Tipo", size=20),
                        ft.Text("Calidad", size=20),
                        ft.Text("FPS/Codec", size=20),
                        ft.Text("Formato", size=20),
                        ft.Text("Peso MB", size=20),
                        ft.Text("Descargar", size=20)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
                padding=15,
                bgcolor=ft.colors.GREY_800
            )
        )

        for sr in streams:
            if(sr.type == "video"):
                listDownActivities.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("Video"),
                                ft.Text(sr.resolution),
                                ft.Text(sr.fps),
                                ft.Text(sr.mime_type),
                                ft.Text(value=f"{sr.filesize_mb} MB"),
                                ft.IconButton(icon=ft.icons.DOWNLOAD,icon_color="blue600",tooltip="Download", on_click=lambda e: Download(sr.itag))
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        padding=15
                    )
                )
            elif(sr.type == "audio"):
                listDownActivities.controls.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("Audio"),
                                ft.Text(sr.abr),
                                ft.Text(sr.audio_codec),
                                ft.Text(sr.mime_type),
                                ft.Text(value=f"{sr.filesize_mb} MB"),
                                ft.IconButton(icon=ft.icons.DOWNLOAD,icon_color="blue600",tooltip="Download", on_click=lambda e: Download(sr.itag))
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY
                        ),
                        padding=15
                    )
                )

    def Download(id):
        yt = YouTube(textfield_URL.value,on_progress_callback=on_progress)
        
        listDownActivities.controls = []
        listActivity.controls.append(DownActivity(yt).ShowActivity())

        estado.value = "Descargando Archivo..."
        estado.color = ft.colors.BLUE
        textfield_PATH_FILE.color = ft.colors.WHITE

        page.update()

        if(textfield_PATH_FILE.value == ""):
            stream = yt.streams.get_by_itag(id).download(output_path=f"{os.path.expanduser('~')}\\Downloads")
        else:
            try:
                stream = yt.streams.get_by_itag(id).download(output_path=textfield_PATH_FILE.value)
            except:
                textfield_PATH_FILE.value = "Directorio Invalido"
                textfield_PATH_FILE.color = ft.colors.RED
                page.update()

    SearchButton = ft.IconButton(icon=ft.icons.SEARCH, on_click=Validacion)
    textfield_URL = ft.TextField(label="URL", width=600)
    textfield_PATH_FILE = ft.TextField(label="Directorio", width=600,tooltip="Coloque un directorio donde desea que se guarde el video/audio (Predeterminado es Download)")

    page.add(
            ft.Row([
                title,
            ],alignment=ft.MainAxisAlignment.CENTER),
            ft.Row(
                controls=[
                    textfield_URL,
                    SearchButton,
                    estado
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row([
                textfield_PATH_FILE
            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Row(
                controls=[
                    progress,
                    label_progress
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ),
            listActivity,
            listDownActivities
    )

ft.app(main)

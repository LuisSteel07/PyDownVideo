import flet as ft
import os
from math import floor
from urllib import error
from pytube import YouTube, Stream, Playlist, exceptions
from DownActivity import DownActivity

DownActivitiesList = list()

def main(page: ft.Page):
    page.title = "PyDownVideo"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.DARK

    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_label = ft.Text("0%")

    progress_grid = ft.Row([
        progress_bar,
        progress_label
    ])

    ThemeIcon = ft.PopupMenuItem("Tema",icon=ft.icons.LIGHT_MODE,on_click= lambda e: Change_Theme(e))
    title = ft.Text(value="PyDownVideo",size=30,weight=ft.FontWeight.BOLD)

    estado = ft.ProgressRing(visible=False)

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

    listDownOptions = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
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

    def Change_Theme(e):
        if(page.theme_mode == ft.ThemeMode.DARK):
            page.theme_mode = ft.ThemeMode.LIGHT
            ThemeIcon.icon = ft.icons.DARK_MODE
        elif(page.theme_mode == ft.ThemeMode.LIGHT):
            page.theme_mode = ft.ThemeMode.DARK
            ThemeIcon.icon = ft.icons.LIGHT_MODE

        page.update()

    def Show_Alert_ERROR(err) -> ft.AlertDialog:
        alert = ft.AlertDialog(
            modal=True,
            adaptive=True,
            title=ft.Text("Error"),
            content=ft.Text(f"Informacion: {err}"),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.close(alert)),
            ],
        )
        
        return alert

    def AppEndListActivity(video: YouTube):
        listActivity.controls.append(
            ft.Row(controls=[
                ft.Image(video.thumbnail_url, width=240),
                ft.Column(controls=[
                    ft.Text(video.title, size=30),
                ])
            ])
        )

    def on_progress(stream: Stream, chunk, bytes_remaining):
        total_filesize = stream.filesize
        bytes_dowloaded = total_filesize - bytes_remaining
        porcent = bytes_dowloaded / total_filesize * 100 

        progress_bar.value = round(porcent) / 100
        progress_label.value = f"{round(porcent)}%"

        page.update()

    def on_complete(data, path: str):
        del DownActivitiesList[0]
        del listActivity.controls[0]

        progress_bar.value = 0
        progress_label.value = "0%"

        page.update()

        AdminListActivities(True)

    def AdminListActivities(stream, path: str = ""):
        page.update()
        if stream == True:
            if len(DownActivitiesList) > 0:
                Download(DownActivitiesList[0].getStream(), DownActivitiesList[0].path)
            if len(DownActivitiesList) == 0:
                estado.visible = False
                textfield_URL.disabled = False
                SearchButton.disabled = False
                page.update()

        else:
            listDownOptions.controls = []
            estado.visible = True
            textfield_URL.disabled = False
            SearchButton.disabled = False

            page.update()

            DownActivitiesList.append(DownActivity(stream,path))

            if len(DownActivitiesList) == 1:
                Download(DownActivitiesList[0].getStream(), DownActivitiesList[0].path)

        page.update()

    def Validacion(e):
        try:
            SearchButton.disabled = True
            textfield_URL.disabled = True
            page.add(progressRing)
            page.update()

            if("list" in textfield_URL.value):
                yt = Playlist(textfield_URL.value)
                DownOptionsPlaylist(yt)
            else:
                yt = YouTube(textfield_URL.value, on_complete_callback=on_complete, on_progress_callback=on_progress)
                DownOptions(yt.streams)
            
            estado.visible = False
            page.update()
        except exceptions.RegexMatchError:
            page.open(Show_Alert_ERROR("URL Inválida"))
            SearchButton.disabled = False
            textfield_URL.disabled = False
            page.remove(progressRing)
            page.update()
        except Exception as err:
            page.open(Show_Alert_ERROR(err))
            SearchButton.disabled = False
            textfield_URL.disabled = False
            page.remove(progressRing)
            page.update()

    def Download(stream: Stream, path: str = ""):
        try:
            if(path != ""):
                listActivity.controls[0].controls[1].controls.append(ft.Row([progress_bar, progress_label]))
                page.update()
                stream.download(path)
            elif(textfield_PATH_FILE.value == ""):
                listActivity.controls[0].controls[1].controls.append(ft.Row([progress_bar, progress_label]))
                page.update()
                stream.download(f"{os.path.expanduser('~')}\\Downloads")
            elif(textfield_PATH_FILE.value != ""):
                listActivity.controls[0].controls[1].controls.append(ft.Row([progress_bar, progress_label]))
                page.update()
                stream.download(textfield_PATH_FILE.value)    
        except error.URLError as err:
            page.open(Show_Alert_ERROR("Revise su red, podría estar desconectado..."))
            listActivity.controls.clear()
            textfield_URL.disabled = False
            SearchButton.disabled = False
            estado.visible = False
            listActivity.controls.clear()
            page.update()
            return -1
        except Exception as err:
            page.open(Show_Alert_ERROR(err))
            textfield_URL.disabled = False
            SearchButton.disabled = False
            estado.value = False
            listActivity.controls.clear()
            page.update()

    def Download_Playlist(playlist: Playlist, type_content: str):
        playlist_path = ""
        listDownOptions.controls = []
        estado.visible = True
        progressRing.visible = False

        page.update()

        try:
            os.mkdir(f"{os.path.expanduser('~')}\\Downloads\\{playlist.title}")
            playlist_path = f"{os.path.expanduser('~')}\\Downloads\\{playlist.title}"
        except FileExistsError as err:
            page.open(Show_Alert_ERROR(f"La carpeta {playlist.title} ya está creada, eliminela y luego inserte de nuevo la playlist"))
            textfield_URL.disabled = False
            SearchButton.disabled = False
            
            if len(DownActivitiesList) == 0:
                estado.visible = False
            page.remove(progressRing)            
            return -1
        except error.URLError as err:
            page.open(Show_Alert_ERROR("Revise su red, podría estar desconectado..."))
            textfield_URL.disabled = False
            SearchButton.disabled = False
            
            if len(DownActivitiesList) == 0:
                estado.visible = False
            page.remove(progressRing)            
            return -1
        except Exception as err:
            page.open(Show_Alert_ERROR(err))
            textfield_URL.disabled = False
            SearchButton.disabled = False
            
            if len(DownActivitiesList) == 0:
                estado.visible = False
            page.remove(progressRing)            
            return -1

        try:
            for video in playlist.videos:
                AppEndListActivity(video)
                video.register_on_progress_callback(on_progress)
                video.register_on_complete_callback(on_complete)

                if(textfield_PATH_FILE.value == ""):
                    if(type_content == "higt"):
                        DownActivitiesList.append(DownActivity(video.streams.get_highest_resolution(),playlist_path))
                    elif(type_content == "low"):
                        DownActivitiesList.append(DownActivity(video.streams.get_lowest_resolution(),playlist_path))
                    elif(type_content == "audio"):
                        DownActivitiesList.append(DownActivity(video.streams.get_audio_only(),playlist_path))
                elif(textfield_PATH_FILE.value != ""):
                    if(type_content == "higt"):
                        DownActivitiesList.append(DownActivity(video.streams.get_highest_resolution(),textfield_PATH_FILE.value))
                    elif(type_content == "low"):
                        DownActivitiesList.append(DownActivity(video.streams.get_lowest_resolution(),textfield_PATH_FILE.value))
                    elif(type_content == "audio"):
                        DownActivitiesList.append(DownActivity(video.streams.get_audio_only(),textfield_PATH_FILE.value))
                
                page.update()
        except Exception as err:
            page.open(Show_Alert_ERROR(err))
            listActivity.controls.clear()
            textfield_URL.disabled = False
            SearchButton.disabled = False
            estado.visible = False
            page.update()
            return -1

        if textfield_PATH_FILE.value == "": AdminListActivities(True, playlist_path)
        else: AdminListActivities(True)

        textfield_URL.disabled = False
        SearchButton.disabled = False
        page.update()

    def DownOptions(streams):
        AppEndListActivity(YouTube(textfield_URL.value))

        listDownOptions.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Tipo")),
                    ft.DataColumn(ft.Text("Calidad")),
                    ft.DataColumn(ft.Text("Tamaño")),
                    ft.DataColumn(ft.Text("Mime_Type")),
                    ft.DataColumn(ft.Text("Acción")),
                ],
                rows=[
                    ft.DataRow([
                        ft.DataCell(ft.Text("Video")),
                        ft.DataCell(ft.Text(streams.get_highest_resolution().resolution)),
                        ft.DataCell(ft.Text(streams.get_highest_resolution().filesize_mb)),
                        ft.DataCell(ft.Text(streams.get_highest_resolution().mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: AdminListActivities(streams.get_highest_resolution()))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Video")),
                        ft.DataCell(ft.Text(streams.get_lowest_resolution().resolution)),
                        ft.DataCell(ft.Text(streams.get_lowest_resolution().filesize_mb)),
                        ft.DataCell(ft.Text(streams.get_lowest_resolution().mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: AdminListActivities(streams.get_lowest_resolution()))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Video")),
                        ft.DataCell(ft.Text(streams[floor(len(streams.filter(type="video")) / 2)].resolution)),
                        ft.DataCell(ft.Text(streams[floor(len(streams.filter(type="video")) / 2)].filesize_mb)),
                        ft.DataCell(ft.Text(streams[floor(len(streams.filter(type="video")) / 2)].mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: AdminListActivities(streams[floor(len(streams.filter(type="video")) / 2)]))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Audio")),
                        ft.DataCell(ft.Text(streams.get_audio_only().abr)),
                        ft.DataCell(ft.Text(streams.get_audio_only().filesize_mb)),
                        ft.DataCell(ft.Text(streams.get_audio_only().mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: AdminListActivities(streams.get_audio_only()))),
                    ]),
                ],
                width=800,
            )
        )
        
        page.remove(progressRing)
        page.update()

    def DownOptionsPlaylist(playlist: Playlist):
        listDownOptions.controls.append(
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
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: Download_Playlist(playlist, "higt"))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Video")),
                        ft.DataCell(ft.Text("Bajo")),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: Download_Playlist(playlist, "low"))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Audio")),
                        ft.DataCell(ft.Text("Alto")),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: Download_Playlist(playlist, "audio"))),
                    ]),
                ]
            )
        )
        page.update()
    
    SearchButton = ft.IconButton(icon=ft.icons.SEARCH, on_click=Validacion)
    textfield_URL = ft.TextField(label="URL", width=600, hint_text="Escriba la URL del video aquí", on_submit=Validacion)

    page.appbar = ft.AppBar(
        title=title,
        leading=ft.Container(content=ft.Image("./python.png",width=120),padding=20),
        leading_width = 100,
        center_title=False,
        toolbar_height=75,
        actions=[
            ft.Container(
                content=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Ruta de Descarga", on_click= lambda e: page.open(config_alert)),
                        ThemeIcon,
                    ]
                )
            )
        ]
    )

    page.add(
            ft.Row(
                controls=[
                    textfield_URL,
                    SearchButton,
                    estado
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            listDownOptions,
            listActivity,
    )

ft.app(main)
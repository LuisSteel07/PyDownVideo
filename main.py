import flet as ft
import os
from math import floor
from urllib import error
from pytubefix import YouTube, Stream, Playlist, exceptions
from DownActivity import DownActivity

DownActivitiesList: list[DownActivity] = []


def main(page: ft.Page):
    page.title = "PyDownVideo"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.DARK

    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_label = ft.Text("0%")

    theme_icon = ft.PopupMenuItem("Tema", icon=ft.icons.LIGHT_MODE, on_click=lambda e: change_theme(e))
    title = ft.Text(value="PyDownVideo", size=30, weight=ft.FontWeight.BOLD)

    estado = ft.ProgressRing(visible=False)

    textfield_path_file = ft.TextField(label="Directorio", width=600,
                                       tooltip="Coloque un directorio donde desea que se guarde el video/audio ("
                                               "Predeterminado es Download)")

    config_alert = ft.AlertDialog(
        modal=True,
        adaptive=True,
        title=ft.Text("Establecer Ruta de Descarga:"),
        content=textfield_path_file,
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(config_alert)),
        ],
    )

    list_activity = ft.Column(
        scroll=ft.ScrollMode.ALWAYS,
        controls=[]
    )

    list_down_options = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        controls=[]
    )

    progress_ring = ft.Row([
        ft.Column([
            ft.Row([
                ft.ProgressRing(),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Buscando Archivo..."),
        ]),
    ], alignment=ft.MainAxisAlignment.CENTER)

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.icon = ft.icons.DARK_MODE
        elif page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.icon = ft.icons.LIGHT_MODE

        page.update()

    def show_alert_error(err) -> ft.AlertDialog:
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

    def on_progress(stream: Stream, chunk, bytes_remaining):
        total_filesize = stream.filesize
        bytes_dowloaded = total_filesize - bytes_remaining
        porcent = bytes_dowloaded / total_filesize * 100

        DownActivitiesList[0].set_progress(round(porcent))

        page.update()

    def on_complete(data, path: str):
        del DownActivitiesList[0]
        del list_activity.controls[0]

        progress_bar.value = 0
        progress_label.value = "0%"

        page.update()

        admin_list_activities(next_process=True)

    def admin_list_activities(stream: Stream = None, path: str = "", next_process: bool = False):
        estado.visible = False
        textfield_url.disabled = False
        search_button.disabled = False
        page.update()
        if next_process:
            if len(DownActivitiesList) > 0:
                download(DownActivitiesList[0].stream[0], DownActivitiesList[0].path)
            if len(DownActivitiesList) == 0:
                estado.visible = False
                page.update()

        else:
            list_down_options.controls = []
            estado.visible = True
            page.update()
            activity = DownActivity(YouTube(textfield_url.value), stream, path)
            list_activity.controls.append(activity.show_activity())

            page.update()
            DownActivitiesList.append(activity)
            if len(DownActivitiesList) == 1:
                download(DownActivitiesList[0].stream[0], DownActivitiesList[0].path)

        page.update()

    def validacion(e):
        try:
            search_button.disabled = True
            textfield_url.disabled = True
            page.add(progress_ring)
            page.update()

            if "list" in textfield_url.value:
                yt = Playlist(textfield_url.value)
                down_options_playlist(yt)
            else:
                yt = YouTube(textfield_url.value, on_complete_callback=on_complete, on_progress_callback=on_progress)
                down_options(yt.streams)

            estado.visible = False
            page.update()
        except exceptions.RegexMatchError:
            page.open(show_alert_error("URL Inválida"))
            search_button.disabled = False
            textfield_url.disabled = False
            page.remove(progress_ring)
            page.update()
        except Exception as err:
            page.open(show_alert_error(err))
            search_button.disabled = False
            textfield_url.disabled = False
            page.remove(progress_ring)
            page.update()

    def download(stream: Stream, path: str = ""):
        try:
            if path != "":
                # list_activity.controls[0].controls[1].controls.append(ft.Row([progress_bar, progress_label]))
                page.update()
                stream.download(path)
            elif textfield_path_file.value == "":
                page.update()
                stream.download(f"{os.path.expanduser('~')}\\Downloads\\")
            elif textfield_path_file.value != "":
                page.update()
                stream.download(textfield_path_file.value)
        except error.URLError:
            page.open(show_alert_error("Revise su red, podría estar desconectado..."))
            list_activity.controls.clear()
            textfield_url.disabled = False
            search_button.disabled = False
            estado.visible = False
            list_activity.controls.clear()
            page.update()
            return -1
        except Exception as err:
            page.open(show_alert_error(f"{type(err)} : {err}"))
            textfield_url.disabled = False
            search_button.disabled = False
            estado.value = False
            list_activity.controls.clear()
            page.update()

    def download_playlist(playlist: Playlist, type_content: str):
        list_down_options.controls = []
        estado.visible = True
        progress_ring.visible = False
        playlist_path = ""

        page.update()

        try:
            os.mkdir(f"{os.path.expanduser('~')}\\Downloads\\{playlist.title}")
            playlist_path = f"{os.path.expanduser('~')}\\Downloads\\{playlist.title}"
        except FileExistsError:
            page.open(show_alert_error(
                f"La carpeta {playlist.title} ya está creada, eliminela y luego inserte de nuevo la playlist"))
            textfield_url.disabled = False
            search_button.disabled = False

            if len(DownActivitiesList) == 0:
                estado.visible = False
            page.remove(progress_ring)

        except error.URLError:
            page.open(show_alert_error("Revise su red, podría estar desconectado..."))
            textfield_url.disabled = False
            search_button.disabled = False

            if len(DownActivitiesList) == 0:
                estado.visible = False
            page.remove(progress_ring)

        except Exception as err:
            page.open(show_alert_error(err))
            textfield_url.disabled = False
            search_button.disabled = False

            if len(DownActivitiesList) == 0:
                estado.visible = False
            page.remove(progress_ring)

        try:
            for video in playlist.videos:
                video.register_on_progress_callback(on_progress)
                video.register_on_complete_callback(on_complete)

                if textfield_path_file.value == "":
                    if type_content == "higt":
                        activity = DownActivity(video, video.streams.get_highest_resolution(), playlist_path)
                        DownActivitiesList.append(
                            DownActivity(video, video.streams.get_highest_resolution(), playlist_path))
                        list_activity.controls.append(activity.show_activity())

                    elif type_content == "low":
                        activity = DownActivity(video, video.streams.get_lowest_resolution(), playlist_path)
                        DownActivitiesList.append(
                            DownActivity(video, video.streams.get_lowest_resolution(), playlist_path))
                        list_activity.controls.append(activity.show_activity())
                    elif type_content == "audio":
                        activity = DownActivity(video, video.streams.get_audio_only(), playlist_path)
                        DownActivitiesList.append(DownActivity(video, video.streams.get_audio_only(), playlist_path))
                        list_activity.controls.append(activity.show_activity())
                elif textfield_path_file.value != "":
                    if type_content == "higt":
                        activity = DownActivity(video, video.streams.get_highest_resolution(),
                                                textfield_path_file.value)
                        DownActivitiesList.append(
                            DownActivity(video, video.streams.get_highest_resolution(), textfield_path_file.value))
                        list_activity.controls.append(activity.show_activity())
                    elif type_content == "low":
                        activity = DownActivity(video, video.streams.get_lowest_resolution(), textfield_path_file.value)
                        DownActivitiesList.append(
                            DownActivity(video, video.streams.get_lowest_resolution(), textfield_path_file.value))
                        list_activity.controls.append(activity.show_activity())
                    elif type_content == "audio":
                        activity = DownActivity(video, video.streams.get_audio_only(), textfield_path_file.value)
                        DownActivitiesList.append(
                            DownActivity(video, video.streams.get_audio_only(), textfield_path_file.value))
                        list_activity.controls.append(activity.show_activity())

                page.update()
        except Exception as err:
            page.open(show_alert_error(err))
            list_activity.controls.clear()
            textfield_url.disabled = False
            search_button.disabled = False
            estado.visible = False
            page.update()

        if textfield_path_file.value == "":
            admin_list_activities(path=playlist_path, next_process=True)
        else:
            admin_list_activities(next_process=True)

    def down_options(streams):
        list_down_options.controls.append(
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
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: admin_list_activities(
                            streams.get_highest_resolution()))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Video")),
                        ft.DataCell(ft.Text(streams.get_lowest_resolution().resolution)),
                        ft.DataCell(ft.Text(streams.get_lowest_resolution().filesize_mb)),
                        ft.DataCell(ft.Text(streams.get_lowest_resolution().mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: admin_list_activities(
                            streams.get_lowest_resolution()))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Video")),
                        ft.DataCell(ft.Text(streams[floor(len(streams.filter(type="video")) / 2)].resolution)),
                        ft.DataCell(ft.Text(streams[floor(len(streams.filter(type="video")) / 2)].filesize_mb)),
                        ft.DataCell(ft.Text(streams[floor(len(streams.filter(type="video")) / 2)].mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD, on_click=lambda e: admin_list_activities(
                            streams[floor(len(streams.filter(type="video")) / 2)]))),
                    ]),
                    ft.DataRow([
                        ft.DataCell(ft.Text("Audio")),
                        ft.DataCell(ft.Text(streams.get_audio_only().abr)),
                        ft.DataCell(ft.Text(streams.get_audio_only().filesize_mb)),
                        ft.DataCell(ft.Text(streams.get_audio_only().mime_type)),
                        ft.DataCell(ft.IconButton(icon=ft.icons.DOWNLOAD,
                                                  on_click=lambda e: admin_list_activities(streams.get_audio_only()))),
                    ]),
                ],
                width=800,
            )
        )

        page.remove(progress_ring)
        page.update()

    def down_options_playlist(playlist: Playlist):
        list_down_options.controls.append(
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
                        ft.DataCell(ft.Text("Bao")),
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

    search_button = ft.IconButton(icon=ft.icons.SEARCH, on_click=validacion)
    textfield_url = ft.TextField(label="URL", width=600, hint_text="Escriba la URL del video aquí",
                                 on_submit=validacion)

    page.appbar = ft.AppBar(
        title=title,
        leading=ft.Container(content=ft.Image("./python.png", width=120), padding=20),
        leading_width=100,
        center_title=False,
        toolbar_height=75,
        actions=[
            ft.Container(
                content=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Ruta de Descarga", on_click=lambda e: page.open(config_alert)),
                        theme_icon,
                    ]
                )
            )
        ]
    )

    page.add(
        ft.Row(
            controls=[
                textfield_url,
                search_button,
                estado
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        list_down_options,
        list_activity,
    )


ft.app(main)

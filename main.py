import os.path
import threading
import time
from urllib import error
from os import remove

import flet as ft
from moviepy.editor import *
from pytubefix import YouTube, Stream, Playlist, exceptions, StreamQuery, Caption

from DownActivity import DownActivity
from DownOption import DownOption
from util import parsing_name_file, wrap_text

DownActivitiesList: list[DownActivity] = []


def main(page: ft.Page):
    page.title = "PyDownVideo"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS
    page.theme_mode = ft.ThemeMode.DARK

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

    list_down_options = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        width=1200,
        controls=[]
    )

    cancel_download_button = ft.IconButton(
        icon=ft.icons.CLOSE,
        icon_size=30,
        disabled=True,
        on_click=lambda e: cancel_download()
    )

    progress_ring = ft.Row([
        ft.Column([
            ft.Row([
                ft.ProgressRing(),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Buscando Archivo..."),
        ]),
    ], alignment=ft.MainAxisAlignment.CENTER)

    captions_options = ft.Dropdown(
        width=250,
        tooltip="Idioma del subtítulo disponible a descargar"
    )

    def change_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon.icon = ft.icons.DARK_MODE
        elif page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon.icon = ft.icons.LIGHT_MODE

        page.update()

    def on_progress_conv(output_path: str, final_size):
        # Hace un tiempo de espera antes de leer el archivo
        # para que pueda encontrar el archivo exportado
        time.sleep(4)

        while True:
            try:
                file_size = os.path.getsize(output_path)
                progress = (file_size / final_size) * 100
                if progress >= 80:
                    break
                DownActivitiesList[0].set_progress_value(progress)
                page.update()
                time.sleep(3)
            except FileNotFoundError:
                time.sleep(10)
                continue

    def cancel_download():
        list_down_options.controls.clear()
        search_button.disabled = False
        textfield_url.disabled = False
        textfield_url.value = ""
        page.update()

    def show_alert_error(err) -> ft.AlertDialog:
        search_button.disabled = False
        textfield_url.disabled = False
        cancel_download_button.disabled = True
        page.remove(progress_ring)

        if len(DownActivitiesList) == 0:
            estado.visible = False

        page.update()

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
            activity = DownActivity(YouTube(textfield_url.value), stream, path)
            list_activity.controls.append(activity.show_activity())

            DownActivitiesList.append(activity)
            page.update()
            if len(DownActivitiesList) == 1:
                download(DownActivitiesList[0].stream[0], DownActivitiesList[0].path)

        page.update()

    def validation(e):
        try:
            search_button.disabled = True
            textfield_url.disabled = True
            cancel_download_button.disabled = False
            page.add(progress_ring)
            page.update()

            if "list" in textfield_url.value:
                yt = Playlist(textfield_url.value)
                down_options_playlist(yt)
            else:
                yt = YouTube(textfield_url.value, on_progress_callback=on_progress)
                down_options(yt, yt.streams)

            estado.visible = False
            page.update()
        except exceptions.RegexMatchError:
            page.open(show_alert_error("URL Inválida"))
        except Exception as err:
            page.open(show_alert_error(f"{type(err)} : {err}"))

    def download(stream: Stream, path: str = ""):
        yt: YouTube = YouTube(textfield_url.value)

        if path != "":
            pass
        elif textfield_path_file.value == "":
            path = f"{os.path.expanduser('~')}\\Downloads\\"
        elif textfield_path_file.value != "":
            path = textfield_path_file.value

        try:
            if stream.type == "audio":
                stream.download(path, mp3=True, filename=parsing_name_file(DownActivitiesList[0].yt.title))
            elif stream.type == "video":
                video_path = stream.download(path, filename=f"{parsing_name_file(DownActivitiesList[0].yt.title)}.mp4")
                if captions_options.value is not None:
                    caption: Caption | None = yt.captions.get(f'{captions_options.value}')
                    if caption is not None:
                        caption.download(title=yt.title, output_path=path)
                if not stream.is_progressive:
                    DownActivitiesList[0].progress_label.value = "Convirtiendo..."
                    page.update()
                    audio_path = yt.streams.get_audio_only().download(path, mp3=True, filename=parsing_name_file(
                        DownActivitiesList[0].yt.title))
                    video = VideoFileClip(video_path)
                    audio = AudioFileClip(audio_path)
                    video.audio = CompositeAudioClip([audio])
                    output_path = f"{path}\\{parsing_name_file(yt.title)}[{stream.resolution}].mp4"

                    total_size = os.path.getsize(video_path) + os.path.getsize(audio_path)
                    t = threading.Thread(target=on_progress_conv, args=(output_path, total_size))
                    t.start()
                    video.write_videofile(
                        filename=output_path, threads=8, fps=30)
                    t.join()
                    remove(video_path)
                    remove(audio_path)
            del DownActivitiesList[0]
            del list_activity.controls[0]
            page.update()
            admin_list_activities(next_process=True)
        except error.URLError:
            page.open(show_alert_error("Revise su red, podría estar desconectado..."))
        except Exception as err:
            page.open(show_alert_error(f"{type(err)} : {err}"))

    def download_playlist(playlist: Playlist, type_content: str):
        list_down_options.controls = []
        estado.visible = True
        progress_ring.visible = False
        playlist_path = ""
        page.update()

        try:
            carpet_name = parsing_name_file(playlist.title)
            if textfield_path_file.value == "":
                os.mkdir(f"{os.path.expanduser('~')}\\Downloads\\{carpet_name}")
                playlist_path = f"{os.path.expanduser('~')}\\Downloads\\{carpet_name}"
            elif textfield_path_file.value != "":
                os.mkdir(f"{textfield_path_file.value}\\{carpet_name}")
                playlist_path = f"{textfield_path_file.value}\\Downloads\\{carpet_name}"

            for video in playlist.videos:
                activity = 0
                video.register_on_progress_callback(on_progress)

                if type_content == "hight":
                    activity = DownActivity(video, video.streams.get_highest_resolution(), playlist_path)
                elif type_content == "low":
                    activity = DownActivity(video, video.streams.get_lowest_resolution(), playlist_path)
                elif type_content == "audio":
                    activity = DownActivity(video, video.streams.get_audio_only(), playlist_path)

                DownActivitiesList.append(activity)
                list_activity.controls.append(activity.show_activity())
                page.update()
        except FileExistsError:
            page.open(show_alert_error(
                f"La carpeta {playlist.title} ya está creada, eliminela y luego inserte de nuevo la playlist"))
        except error.URLError:
            page.open(show_alert_error("Revise su red, podría estar desconectado..."))
        except Exception as err:
            page.open(show_alert_error(f"{type(err)} : {err}"))

        if textfield_path_file.value == "":
            admin_list_activities(path=playlist_path, next_process=True)
        else:
            admin_list_activities(next_process=True)

    def create_rows(streams: StreamQuery) -> list[ft.DataRow]:
        rows: list[ft.DataRow] = []
        for stream in streams:
            rows.append(DownOption(stream).show_option(admin_list_activities))
        return rows

    def down_options(yt: YouTube, streams):
        for caption in yt.captions.all():
            captions_options.options.append(
                ft.dropdown.Option(caption.code, caption.name)
            )

        list_down_options.controls.append(
            ft.Row(
                controls=[
                    ft.Image(yt.thumbnail_url, width=240),
                    ft.Text(wrap_text(yt.title), size=30),
                ],
                spacing=30
            )
        )

        list_down_options.controls.append(
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Tipo")),
                    ft.DataColumn(ft.Text("Calidad")),
                    ft.DataColumn(ft.Text("Tamaño")),
                    ft.DataColumn(ft.Text("Extensión")),
                    ft.DataColumn(ft.Text("Acción")),
                ],
                rows=create_rows(streams),
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
                                                  on_click=lambda e: download_playlist(playlist, "hight"))),
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

    search_button = ft.IconButton(icon=ft.icons.SEARCH, on_click=validation)
    textfield_url = ft.TextField(label="URL", width=600, hint_text="Escriba la URL del video aquí",
                                 on_submit=validation)

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
                captions_options,
                cancel_download_button,
                estado
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        list_down_options,
        list_activity,
    )


ft.app(main)

import flet as ft
from pytube import YouTube, Stream
from DownActivity import DownActivity

def main(page: ft.Page):
    page.title = "PyDownVideo"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS

    title = ft.Text(value="PyDownVideo",size=30,weight=ft.FontWeight.BOLD)

    progress = ft.ProgressBar(width=400, value=0)
    label_progress = ft.Text("0%")

    listDownActivities = ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[]
        )

    listActivity = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=[]
        )

    progressRing = ft.Column([
        ft.ProgressRing(),
        ft.Text("Buscando Archivo..."),
    ])

    def on_progress(stream: Stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_down = total_size - bytes_remaining
        porcent = bytes_down / total_size * 100

        progress.value = round(porcent,2) * 0.01
        label_progress.value = f"{round(porcent,2)}%"

        page.update()

    def Validacion(e) :
        textfield_URL.color = "white"
        progress.value = 0
        label_progress.value = "0%"

        try:
            yt = YouTube(textfield_URL.value,on_progress_callback=on_progress)
            print(yt.title)

            page.add(progressRing)

            listActivity.controls.append(DownActivity(yt.title, yt.thumbnail_url).ShowActivity())
            print("hello")
            stream = yt.streams.get_lowest_resolution()
            print("hello")

            page.remove(progressRing)
            stream.download()
            page.update()

            # OptionsDown(yt.streams)
        except Exception as err:
            textfield_URL.value = "URL Invalida"
            textfield_URL.color = ft.colors.RED
            print(err)
            page.remove(progressRing)
            page.update()

    # def Download(id):
    #     yt = YouTube(textfield_URL.value,on_complete_callback=on_progress)

    #     Activity = DownActivity(yt.title, yt.thumbnail_url, yt.streams.get_by_itag(id))

    #     listActivity.controls.append(Activity.ShowActivity())
    #     listDownActivities.controls = []

    #     stream = yt.streams.get_by_itag(id)

    #     stream.download()

    #     page.update()

    def OptionsDown(streams):
        print("Hola")
        print(streams)
        print("Hola")
        for sr in streams:
            if(sr.type == "video"):
                listDownActivities.controls.append(
                    ft.Card(
                        content=ft.Row(controls=[
                                ft.Text("Video"),
                                ft.Text(sr.resolution),
                                ft.Text(sr.fps),
                                ft.Text(value=f"{sr.filesize_mb} MB"),
                                ft.IconButton(icon=ft.icons.DOWNLOAD,icon_color="blue600",tooltip="Download", on_click=lambda e: Download(sr.itag))
                            ]
                        )
                    )
                )
            elif(sr.type == "audio"):
                listDownActivities.controls.append(
                    ft.Card(
                        content=ft.Row(controls=[
                                ft.Text("Audio"),
                                ft.Text(sr.abr),
                                ft.Text(sr.audio_codec),
                                ft.Text(value=f"{sr.filesize_mb} MB"),
                                ft.IconButton(icon=ft.icons.DOWNLOAD,icon_color="blue600",tooltip="Download")
                            ]
                        )
                    )
                )

    textfield_URL = ft.TextField(label="URL", width=600)

    page.add(
            title,
            ft.Row(controls=[
                textfield_URL,
                ft.IconButton(icon=ft.icons.SEARCH, on_click=Validacion),
            ]),
            ft.Row([
                progress,
                label_progress,
            ]),
            listActivity,
            listDownActivities,
    )

ft.app(main)

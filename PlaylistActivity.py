import flet as ft

from pytubefix import Playlist
from DownActivity import DownActivity


class SelectedVideo:
    def __init__(self, _video: DownActivity):
        self.video = _video
        self.is_selected = ft.Checkbox(tooltip="Seleccionar video", value=True)


class PlaylistActivity:
    def __init__(self, _playlist: Playlist):
        self.videos: list[SelectedVideo] = []

        for video in _playlist.videos:
            self.videos.append(SelectedVideo(DownActivity(video, video.streams[0])))

    def show_panel_selection(self, get_selected_videos) -> ft.ListView:
        list_view = ft.ListView()
        for control in self.videos:
            list_view.controls.append(
                ft.Row([
                    control.is_selected,
                    ft.Image(control.video.yt.thumbnail_url, width=320),
                    ft.Text(control.video.yt.title, size=20),
                ])
            )

        list_view.controls.append(ft.TextButton("Seleccionar", on_click=lambda e: get_selected_videos(self.videos)))

        return list_view

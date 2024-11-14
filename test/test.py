import subprocess
import sys

video_file = 'C:\\Users\\Luis\\Documents\\Trabajo\\PyDownVideo\\test\\La programación está por despegar el 2025.mp4'
audio_file = 'C:\\Users\\Luis\\Documents\\Trabajo\\PyDownVideo\\test\\La programación está por despegar el 2025.mp3'

# https://www.youtube.com/watch?v=PGpL5hYpY1o

# cmd = "set path_build=%CD% %path_build%\\tools\\ffmpeg.exe -?"
cmd = f'.\\tools\\ffmpeg.exe -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4'
subprocess.run(cmd, shell=True)

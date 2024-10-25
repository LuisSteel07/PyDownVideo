import os
import threading
import time
from math import floor

path = "C:\\Users\\Luis\\Downloads\\Nextars - Panic() EP\\Nextars - Panic().mp3"
size = os.path.getsize(path)
print("Tamaño del archivo: {:.2f} mb".format(file_size / 1000000))


def on_progress_conv(output_path: str, final_size):
    while True:
        try:
            file_size = os.path.getsize(output_path)
            if file_size >= (final_size - 0.5):
                break
            porcent = file_size / final_size
            lista_video[0].progress_bar.value = floor(porcent)
            page.update()
            time.sleep(3)
        except FileNotFoundError as e:
            time.sleep(10)


t = threading.Thread(target=on_progress_conv, args=(path, size,))
t.start()

# More code

t.join()

# import time
#
#
# def on_convertion_progress(file: str):
#
#
#
def worker(name):
    print(f"{name} started")
    time.sleep(10)  # Simula trabajo
    print(f"{name} finished")


threads = []

for i in range(3):
    t = threading.Thread(target=worker, args=(f"Thread-{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("All threads finished")

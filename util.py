from googletrans import Translator
from httpcore import ConnectTimeout


def parsing_name_file(title: str) -> str | None:
    return (((((((((title.replace("/", "")).replace("\\", "")).replace(":", "")).replace("*",
                                                                                         "")).replace(
        "?", "")).replace("\"", "")).replace("<", "")).replace(">", "")).replace("|", "")).strip()


def convert_file(video_path: str, audio_path: str, out_path: str):
    pass


# def translation_subs(relative_path: str, path: str, name: str, lang: str):
#     with open(path, 'r') as subs:
#         translator = Translator()
#
#         with open(f"{relative_path}\\{name}({lang}).srt", 'w') as tran_subs:
#             try:
#                 while True:
#                     numero_secuencia = subs.readline().strip()
#                     if not numero_secuencia:
#                         break
#                     tiempos = subs.readline().strip()
#                     textos = []
#                     linea = subs.readline().strip()
#                     while linea:
#                         textos.append(linea.replace("\n", ""))
#                         linea = subs.readline().strip()
#                     tran_subs.write(f"{numero_secuencia} \n")
#                     tran_subs.write(f"{tiempos} \n")
#                     tran_subs.write(f"{translator.translate(textos[0], dest=lang).text} \n")
#                     print(numero_secuencia)
#             except TypeError:
#                 pass
#             except ConnectTimeout as e:
#                 return e

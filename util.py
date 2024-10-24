from googletrans import Translator
from httpcore import ConnectTimeout


def parsing_name_file(title: str) -> str | None:
    return (((((((((title.replace("/", "")).replace("\\", "")).replace(":", "")).replace("*",
                                                                                         "")).replace(
        "?", "")).replace("\"", "")).replace("<", "")).replace(">", "")).replace("|", "")).strip()

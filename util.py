def parsing_name_file(title: str) -> str | None:
    return (((((((((title.replace("/", "")).replace("\\", "")).replace(":", "")).replace("*",
                                                                                         "")).replace(
        "?", "")).replace("\"", "")).replace("<", "")).replace(">", "")).replace("|", "")).strip()


def wrap_text(text: str, limit: int = 45) -> str:
    if len(text) > limit:
        text = text[0:limit-1] + " ..."
    return text

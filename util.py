def parsing_name_file(title: str) -> str | None:
    return (((((((((title.replace("/", "")).replace("\\", "")).replace(":", "")).replace("*",
                                                                                         "")).replace(
        "?", "")).replace("\"", "")).replace("<", "")).replace(">", "")).replace("|", "")).strip()


def wrap_text(text: str) -> str:
    if len(text) > 45:
        text = text[0:45] + " ..."
    return text

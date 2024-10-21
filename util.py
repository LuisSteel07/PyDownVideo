def parsing_name_file(title: str) -> str | None:
    return (((((((((title.replace("/", "")).replace("\\", "")).replace(":", "")).replace("*",
                                                                                         "")).replace(
        "?", "")).replace("\"", "")).replace("<", "")).replace(">", "")).replace("|", "")).strip()

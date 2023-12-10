from src.infrastructure import application_settings


def is_allowed_file(filename: str) -> bool:
    allowed_extensions = application_settings.allowed_extensions.split(";")
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

__all__ = ["get_template"]

TEMPLATE_FILE_PATH = "data/templates/report/report.html"


def get_template():
    with open(TEMPLATE_FILE_PATH, "r", encoding="utf-8") as file:
        html_content = file.read()

    return html_content

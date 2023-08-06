import datetime
def get_post(title, authors, abstract, pdflink, bibtex, date, categories, format_path=None):
    assert format_path is not None

    with open(format_path, "r") as f:
        format = f.read()

    return eval(format)
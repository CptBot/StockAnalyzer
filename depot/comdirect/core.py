from pdfplumber import PDF


def analyze(pdf: PDF):
    text = pdf.pages[0].extract_text()
    for line in text.split("\n"):
        if line.lower().__contains__("WKN: "):
            print(line)

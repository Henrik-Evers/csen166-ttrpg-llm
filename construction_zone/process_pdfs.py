"""
Run this script just once to convert any PDFs to txt.
It's not perfect, but oh well.
"""


import fitz  # PyMuPDF


DIR_PREFIX = './source_docs/'

# Thank you to the Google search AI for the vibes
def pdf_to_text(pdf_path, text_path):
    try:
        pdf_document = fitz.open(DIR_PREFIX + pdf_path)
        with open(DIR_PREFIX + text_path, "w", encoding="utf-8") as text_file:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text()
                text_file.write(text)
        pdf_document.close()
        print(f"Successfully extracted text from '{pdf_path}' to '{text_path}'")
    except Exception as e:
          print(f"An error occurred: {e}")


# Convert the files
pdf_to_text("Pathfinder 2nd Edition- Core Rulebook.pdf", "Pathfinder 2e Rules.txt")
pdf_to_text("SRD_CC_v5.2.1.pdf", "DnD 5e Rules.txt")
pdf_to_text("World Name.pdf", "World Name.txt")
pdf_to_text("DELVE_PDF_5E.pdf", "Delve 5e.txt")

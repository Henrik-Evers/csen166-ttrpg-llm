import os
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

D_PATH = './data'
RULES_PATH = 'rules'
ADVENTURE_PATH = 'adventure'
CHARS_PATH = 'characters'


# Gets the data from all .txt, .png, .jpg, .jpeg, and .pdf files.
# PDFs will be converted to .txt or .jpg and the source file deleted.
def get_data_from_dir(sub_path):
    data = ''
    images = []
    for filename in os.listdir(os.path.join(D_PATH, sub_path)):
        file_path = os.path.join(D_PATH, sub_path, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a subdirectory
            if file_path.endswith('.txt'):
                with open(file_path, 'r', errors='ignore') as file:
                    data += '\n' + file.read()

            if file_path.endswith('.png') or file_path.endswith('jpeg') or file_path.endswith('jpg'):
                images.append(file_path)
            
            if file_path.endswith('.pdf'):
                print('Converting file: ' + file_path)
                if os.path.basename(file_path).startswith('i'): # Convert to images if marked
                    print('to image')
                    imgs = convert_from_path(file_path, poppler_path=os.getenv('POPPLER_PATH'))
                    for i in range(len(imgs)):
                        i_path = file_path[:-4] + str(i) + '.jpg'
                        imgs[i].save(i_path, 'JPEG')
                        images.append(i_path)
                    os.remove(file_path)
                else: # Default to text because it's faster
                    print('to text')
                    pdf_document = fitz.open(file_path)
                    with open(file_path[:-4] + '.txt', "w", encoding="utf-8") as text_file:
                        for page_num in range(pdf_document.page_count):
                            page = pdf_document[page_num]
                            text = page.get_text()
                            text_file.write(text)
                            data += '\n' + text
                    pdf_document.close()
                    os.remove(file_path)
    
    return data, images


# Run to get the text and images from the data directory.
def process():
    rules_data, rules_images = get_data_from_dir(RULES_PATH)
    adventure_data, adventure_images = get_data_from_dir(ADVENTURE_PATH)
    chars_data, chars_images = get_data_from_dir(CHARS_PATH)

    return (rules_data, rules_images,
            adventure_data, adventure_images,
            chars_data, chars_images)

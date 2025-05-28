import os
from pdf2image import convert_from_path
from dotenv import load_dotenv

load_dotenv()

D_PATH = './data'
RULES_PATH = 'rules'
ADVENTURE_PATH = 'adventure'
CHARS_PATH = 'characters'

def get_data_from_dir(sub_path):
    data = ''
    images = []
    for filename in os.listdir(os.path.join(D_PATH, sub_path)):
        file_path = os.path.join(D_PATH, sub_path, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a subdirectory
            if file_path.endswith('.pdf'):
                print(file_path)
                imgs = convert_from_path(file_path, poppler_path=os.getenv('POPPLER_PATH'))
                for i in range(len(imgs)):
                    i_path = file_path[:-4] + str(i) + '.jpg'
                    imgs[i].save(i_path, 'JPEG')
                    images += i_path
                    print('  +' + i_path)
                os.remove(file_path)
    return data, images

rules_data, rules_images = get_data_from_dir(RULES_PATH)
adventure_data, adventure_images = get_data_from_dir(ADVENTURE_PATH)
chars_data, chars_images = get_data_from_dir(CHARS_PATH)

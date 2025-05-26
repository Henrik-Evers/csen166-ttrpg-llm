from ollama import chat
import os


# Collect information from the files provided in the data subdirectory.
D_PATH = './data'
RULES_PATH = 'rules'
ADVENTURE_PATH = 'adventure'
CHARS_PATH = 'characters'

def get_data_from_dir(sub_path):
    data = ''
    images = []
    for filename in os.listdir(os.path.join(D_PATH, sub_path)):
        file_path = os.path.join(D_PATH, filename)
        if os.path.isfile(file_path):  # Ensure it's a file, not a subdirectory
            print(file_path)
            if file_path.endswith('.txt'):
                with open(file_path, 'r', errors='ignore') as file:
                    data += file.read()
            if file_path.endswith('.png') or file_path.endswith('jpeg'):
                images += file_path
    return data, images

rules_data, rules_images = get_data_from_dir(RULES_PATH)
adventure_data, adventure_images = get_data_from_dir(ADVENTURE_PATH)
chars_data, chars_images = get_data_from_dir(CHARS_PATH)


MODEL_NAME = 'app-model'

# This gives some initial messages to set the stage
# We can't include file contents in the Modelfile, so we include here.
messages = []
    # {
    #     'role': 'system',
    #     'content': 'These are the game rules: ' + rules_data
    # },
    # {
    #     'role': 'system',
    #     'content': 'Please make sure to always follow the rules. Whenever you are given a prompt, check the rules to see if they tell you how to respond. These rules are important and must be followed exactly.'
    # },
    # {
    #     'role': 'system',
    #     'content': 'Here is a document describing the world and adventure you will be running today: ' + adventure_data
    # },
    # {
    #     'role': 'system',
    #     'content': 'Please follow the adventure document during our chat. Your response should use information in the adventure document when relevant. If something is not mentioned, think of what would make the most sense based on what you already know.'
    # },
    # {
    #     'role': 'system',
    #     'content': 'These are the source documents you will be running the game based on: ' + data
    # },
    # {
    #     'role': 'system',
    #     'content': 'Please look at these images. They contain the player characters.',
    #     'images': images
    # },
    # {
    #     'role': 'system',
    #     'content': '''
    #     Please follow these documents as best as you can. Whenever you are given a prompt, check the source documents to see if they tell you how to respond.
    #     If your response is not specified, think of what would make the most sense based on what you already know.
    #     '''
    # }
# ]

if rules_data != '':
    messages.append({
        'role': 'system',
        'content': 'These are the game rules: ' + rules_data,
        'images': rules_images
    })

if adventure_data != '':
    messages.append({
        'role': 'system',
        'content': 'Here is information describing the world and adventure you will be running today: ' + adventure_data,
        'images': adventure_images
    })

if chars_data != '':
    messages.append({
        'role': 'system',
        'content': 'These are the characters who will be playing in the adventure: ' + chars_data,
        'images': chars_images
    })

if rules_data != '' or adventure_data != '' or chars_data != '':
    messages.append({
        {
            'role': 'system',
            'content':
            '''
            Please follow these documents as best as you can. Whenever you are given a prompt, check the source documents to see if they tell you how to respond.
            If your response is not specified, think of what would make the most sense based on what you already know.
            '''
        }
    })


# Initial input to give the user an introduction
user_input = 'I\'m ready to start playing! Can you give a quick summary of the characters and the adventure, then get us started?'

# Loop forever until the user says /exit.
print('Type /exit to terminate the program.')
while user_input != '/exit':
    response = ''
    for part in chat(MODEL_NAME, messages=[*messages, {'role': 'user', 'content': user_input}], stream=True):
        print(part['message']['content'], end='', flush=True)
        response += part['message']['content']
    print()

    # Add the prompt and response to the history
    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response},
    ]

    user_input = input('>> ')

# TODO:
# - More commands beyond just /exit would be great. Maybe we can use /load to load new documents from the directories, and /save to save the changes from this session to a file? For the save, send a prompt to the thing but then pipe the output to a file rather than printing.
# - Fine-tune the system prompts and parameters to make it better.
# - Once home, get a vision model to process images.
# - Include the file conversion within this script. Will also need to convert PDFs to PNGs, at least temporarily, to be passed to the model.

from ollama import chat
import os

MODEL_NAME = 'app-model'

# Collect information from the files provided in the data subdirectory.
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
            if file_path.endswith('.txt'):
                with open(file_path, 'r', errors='ignore') as file:
                    data += file.read()
            if file_path.endswith('.png') or file_path.endswith('jpeg') or file_path.endswith('jpg'):
                images.append(file_path)
    return data, images

rules_data, rules_images = get_data_from_dir(RULES_PATH)
adventure_data, adventure_images = get_data_from_dir(ADVENTURE_PATH)
chars_data, chars_images = get_data_from_dir(CHARS_PATH)


# This gives some initial messages to set the stage
# We can't include file contents in the Modelfile, so we include here.
messages = []

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

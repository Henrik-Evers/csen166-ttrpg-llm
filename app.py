from ollama import chat
import input_processing

MODEL_NAME = 'app-model'
CHARSHEET_MODEL = 'app-charsheet-reader'


# Collect information from the files provided in the data subdirectory.
(rules_data, rules_images,
adventure_data, adventure_images,
chars_data, chars_images) = input_processing.process()


# Helper function to perform a chat request on demand.
def do_chat(messages, model=MODEL_NAME, show=True):
    response = ''
    for part in chat(model, messages=messages, stream=True):
        if show:
            print(part['message']['content'], end='', flush=True)
        response += part['message']['content']
    print()

    return [
        {'role': 'assistant', 'content': response},
    ]


# Message history
messages = []

# Set initial message history / pre-emptive prompts to include input data.
if rules_data != '' or rules_images != []:
    messages.append({
        'role': 'system',
        'content': 'These are the game rules: ' + rules_data,
        'images': rules_images
    })

if adventure_data != '' or adventure_images != []:
    messages.append({
        'role': 'system',
        'content': 'Here is information describing the world and adventure you will be running today: ' + adventure_data,
        'images': adventure_images
    })

if chars_data != '' or chars_images != []:
    msg = {
        'role': 'system',
        'content': 'You will read and respond with the following pieces of information: name, level, race, class, background, personality traits, ideals, bonds, and flaws. You will decribe what is written about the character\'s past. Include their name in your response. Do not mention their equipment or inventory.' + chars_data,
        'images': chars_images
    }
    messages += [msg, do_chat([msg], model=CHARSHEET_MODEL)]
else:
    msg = {
        'role': 'system',
        'content': 'Please generate four characters to be used in the adventure. Include their name, race, and class, and make them level 1 unless directed otherwise. Give them a backstory connected to the adventure.'
    }
    messages += [msg, do_chat([*messages, msg], model=MODEL_NAME)]

if rules_data != '' or adventure_data != '' or chars_data != '':
    messages.append({
        'role': 'system',
        'content':
        '''
        Please follow these documents as best as you can. Whenever you are given a prompt, check the source documents to see if they tell you how to respond.
        If your response is not specified, think of what would make the most sense based on what you already know.
        '''
    })


# Initial input to give the user an introduction
print('\n\nbreak\n\n')
msg = {
    'role': 'user',
    'content': 'I am ready to start playing! Can you give a quick summary of the player character(s) and adventure, then get us started?'
}
messages += [msg, do_chat([*messages, msg], model=MODEL_NAME)]


# Loop prompt -> response, until instructed to stop.
print('Type /exit to terminate the program.')
while True:
    user_input = input('>> ')

    # Commands
    if user_input.startswith('/'):
        if user_input == '/exit':
            break
    
    # Normal message
    else:
        response = ''
        for part in chat(MODEL_NAME, messages=[*messages, {'role': 'user', 'content': user_input, 'images': chars_images}], stream=True):
            print(part['message']['content'], end='', flush=True)
            response += part['message']['content']
        print('')

        # Add the prompt and response to the history
        messages += [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': response},
        ]


# TODO:
# - More commands beyond just /exit would be great. Maybe we can use /load to load new documents from the directories, and /save to save the changes from this session to a file? For the save, send a prompt to the thing but then pipe the output to a file rather than printing.
# - Fine-tune the system prompts and parameters to make it better.
# - Include the file conversion within this script. Will also need to convert PDFs to PNGs, at least temporarily, to be passed to the model.
# - When uploading files by GUI - mark whether rules, adventure, or character. Have it check and, if it's a PDF, mark whether text-heavy or image-heavy (to control how it's converted).

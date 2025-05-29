from ollama import chat
import input_processing
import os

MODEL_NAME = 'app-model'
CHARSHEET_MODEL = 'app-charsheet-reader'

SAVE_PATH = './save.txt'


# Get the environment ready to the point where the user can start sending messages.
def setup():
    global messages, chars_images

    # Collect information from the files provided in the data subdirectory.
    (rules_data, rules_images,
    adventure_data, adventure_images,
    chars_data, char_images) = input_processing.process()
    chars_images = char_images


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


# Perform a prompt and deliver the response.
def send_msg(user_input):
    global messages, chars_images

    # Commands
    if user_input.startswith('/'):
        if user_input.startswith('/exit'):
            yield -1
        if user_input.startswith('/save'):
            if os.path.exists(SAVE_PATH):
                os.remove(SAVE_PATH)
            with open(SAVE_PATH, "w", encoding="utf-8") as save_file:
                save_file.write(chat(MODEL_NAME, messages=[*messages, {'role': 'system', 'content': '''
                                                                       Please summarize everything that has happened in this session as if you were going to hand control over to another dungeon master. Focus on key interactions, changes in the world, and plot development and character development. Make sure to include any consequences of these events.
                                                                       '''}])['message']['content'])
            yield 0
        if user_input == '/help' or user_input =='/':
            yield 'The following slash commands are available:\n/help to see this message.\n/save to save a summary of the session to the project directory/saves.\n/exit to close the program.'
    
    # Normal message
    else:
        response = ''
        for part in chat(MODEL_NAME, messages=[*messages, {'role': 'user', 'content': user_input, 'images': chars_images}], stream=True):
            yield part['message']['content']
            response += part['message']['content']

        # Add the prompt and response to the history
        messages += [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': response},
        ]


def main():
    global messages

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
            for part in chat(MODEL_NAME, messages=[*messages, {'role': 'user', 'content': user_input}], stream=True):
                print(part['message']['content'], end='', flush=True)
                response += part['message']['content']
            print('')

            # Add the prompt and response to the history
            messages += [
                {'role': 'user', 'content': user_input},
                {'role': 'assistant', 'content': response},
            ]


if __name__ == "__main__":
    setup()
    main()

# TODO:
# - More commands beyond just /exit would be great. Maybe we can use /load to load new documents from the directories, and /save to save the changes from this session to a file? For the save, send a prompt to the thing but then pipe the output to a file rather than printing.
# - Fine-tune the system prompts and parameters to make it better.

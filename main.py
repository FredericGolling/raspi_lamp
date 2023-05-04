import requests
import neopixel
import board
import time

# Replace <BOT_TOKEN> with your bot's token
bot_token = '6090202726:AAGSnk8RW3HuZCSTSZITHWyY_swzaBFbyFM'
Ignatius_ID = '1683149821'


def handle_update(update):
    # Extract the chat ID and message text from the update
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']

    
    text_list = message_text.split()
    if len(text_list) > 1:
        if text_list[0] == '+':
            colour = text_list[1]
            add_colour(colour)
            write_message(Ignatius_ID, 'adding colour')

    # Do something with the message text, such as controlling the ESP32
    if message_text == '/on':
        write_message(Ignatius_ID, '/on received')
        one_colour(warmwhite)
       
    elif message_text == '/off':
        write_message(Ignatius_ID, '/off received')
        turn_off()

        

    elif message_text == 'red' or message_text == 'green' or message_text == 'blue' or message_text == 'warmwhite' or message_text == 'coldwhite' or message_text == 'purple':
        write_message(Ignatius_ID, f'{message_text} received')
        one_colour(str(message_text))

    elif message_text == '/red_pulse':
        write_message(Ignatius_ID, f'{message_text} received')
        


def add_colour(colour):
    global active_fill
  
    if colour == 'red':
        if active_fill[0] < max_brightness-add_scale:
            active_fill[0] += add_scale
            update_all()

    if colour == 'green':
        if active_fill[1] < max_brightness-add_scale:
            active_fill[1] += add_scale
            update_all()

    if colour == 'blue':
        if active_fill[2] < max_brightness-add_scale:
            active_fill[2] += add_scale
            update_all()

def update_all():
    global active_fill
    print('updated')
    strip.fill((active_fill[0], active_fill[1], active_fill[2]))

def reset_fill():
    global active_fill
    print('reset')

    active_fill = [0,0,0]


def turn_off():
    reset_fill()
    update_all()


def write_message(id, text):
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': id, 'text': text}
    response = requests.post(url, data=data)
    

def neopixel_test():

    # Set the color of the first LED to red
    strip[0] = (255, 0, 0)  # (R, G, B, W) values for sk6812 LED

    # Set the color of the second LED to green
    strip[1] = (0, 255, 0)

    # Set the color of the third LED to blue
    strip[2] = (0, 0, 255)

    # Update the LED strip
    strip.show()


def one_colour(col):
    global active_fill
    reset_fill()

    if col == 'red':
        active_fill[0] = max_brightness

    elif col == 'green':
        active_fill[1] = max_brightness

    elif col == 'blue':
        active_fill[2] = max_brightness

    elif col == 'warmwhite':
        active_fill[0] = 243
        active_fill[1] = 231
        active_fill[2] = 211

    elif col == 'coldwhite':
        active_fill[0] = 244
        active_fill[1] = 253
        active_fill[2] = 255


    elif col == 'purple':
        active_fill[0] = 160
        active_fill[1] = 32
        active_fill[2] = 240

    

    update_all()

################

# Configure the LED strip
num_leds = 15
led_pin = board.D18
strip = neopixel.NeoPixel(led_pin, num_leds, bpp=3)
max_brightness = int(255 * 0.66)


active_fill = []
add_scale = 20
decr_scale = add_scale/2


#################

reset_fill()
update_all()

# Start a loop to check for updates from the Telegram Bot API
last_update_id = 0

write_message(Ignatius_ID, 'Power on')

while True:
    try:
        url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
        
        if last_update_id != 0:
            url += '?offset={}'.format(last_update_id)

        response = requests.get(url)
        messages = response.json()['result']
        
        for message in messages:
            message_text = message['message']['text']
            message_chat_id = message['message']['chat']['id']
            last_update_id = message['update_id'] + 1

            handle_update(message)

            if message_chat_id != 1683149821:
                write_message(Ignatius_ID, f'Received message: {message_text}')
        
        # Wait for 1 second before checking for new messages again
        time.sleep(1)


    except Exception as e:
        print(f'Error occurred: {e}')
        # Wait for 5 seconds before trying again
        time.sleep(5)


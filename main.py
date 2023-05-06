
# Imports
import requests
import neopixel
import board
import time

# Bot Setup
bot_token = '6090202726:AAGSnk8RW3HuZCSTSZITHWyY_swzaBFbyFM'
Ignatius_ID = '1683149821'


# Function, that reacts to incoming messages
def handle_update(update):
    # Extract information on the new message
    chat_id = update['message']['chat']['id']
    message_text = update['message']['text']

    # If it's two words...
    text_list = message_text.split()
    if len(text_list) > 1:
        if text_list[0] == '+':
            colour = text_list[1]
            add_colour(colour)
            write_message(Ignatius_ID, 'adding colour')

    # If it's one word...
    if message_text == '/on':
        write_message(Ignatius_ID, '/on received')
        one_colour('warmwhite')
       
    elif message_text == '/off':
        write_message(Ignatius_ID, '/off received')
        turn_off()

    elif message_text == 'red' or message_text == 'green' or message_text == 'blue' or message_text == 'warmwhite' or message_text == 'coldwhite' or message_text == 'purple':
        write_message(Ignatius_ID, f'{message_text} received')
        one_colour(str(message_text))

    elif message_text == '/red_pulse':
        write_message(Ignatius_ID, f'{message_text} received')
        

# To add a preset amount of a specific colour component to the active configurations (on all pixels)
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

# Load the active_fill list onto the strip after editing it
def update_all():
    global active_fill
    print('updated')
    strip.fill((active_fill[0], active_fill[1], active_fill[2]))

# replace the active_fill list with an empty list to start clean for colour presets
def reset_fill():
    global active_fill
    print('reset')

    active_fill = [0,0,0]

# simple function for shutdown
def turn_off():
    reset_fill()
    update_all()

# To handle sending a text through the 'requests' library
def write_message(id, text):
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': id, 'text': text}
    response = requests.post(url, data=data)
    
# Initial test from the official adafruit webpage for testing the light strip
def neopixel_test():

    # Set the color of the first LED to red
    strip[0] = (255, 0, 0)  # (R, G, B, W) values for sk6812 LED

    # Set the color of the second LED to green
    strip[1] = (0, 255, 0)

    # Set the color of the third LED to blue
    strip[2] = (0, 0, 255)

    # Update the LED strip
    strip.show()

# Setting a single colour for all pixels on the strip
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

# Configure variables for colour addition and fill function
active_fill = []
add_scale = 20
decr_scale = add_scale/2


################# 

# Start-Up procedure
reset_fill()
update_all()
last_update_id = 0
write_message(Ignatius_ID, 'Power on')


# Infinite loop as a message handler for checking updates fromt he API and forwarding them to the handle_message() function 
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


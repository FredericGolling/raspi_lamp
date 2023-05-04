import urequests
import ujson
#import machine
import neopixel
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
       
    elif message_text == '/off':
        write_message(Ignatius_ID, '/off received')
        

    elif message_text == 'red' or message_text == 'green' or message_text == 'blue':
        write_message(Ignatius_ID, f'{message_text} received')

#        one_colour(str(message_text))

    elif message_text == '/red_pulse':
        write_message(Ignatius_ID, f'{message_text} received')
   
    
def write_message(id, text):
    response_data = {
        'chat_id': id,
        'text': text
    }
    response_url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
    response = urequests.post(response_url, json=response_data)
    
def add_colour(colour):
    global active_fill
    '''
    pin = 0

    match colour:
        case 'green':
            pin = 1
    '''

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

    strip.fill((active_fill[0], active_fill[1], active_fill[2]))

def reset_fill():
    global active_fill

    active_fill = [0,0,0]


def turn_off():
    reset_fill()
    update_all()


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
    print(type(col))
    print(col)

    if col == 'red':
        strip.fill((max_brightness, 0, 0))
        active_fill = [max_brightness,0,0]

    elif col == 'green':
        strip.fill((0, max_brightness, 0))
        active_fill = [0,max_brightness,0]

    elif col == 'blue':
        strip.fill((0, 0, max_brightness))
        active_fill = [0,0,max_brightness]

    strip.show()

################

# Configure the LED strip
num_leds = 15
pin_nr = 26  # Replace with the GPIO pin number to which the LED strip is connected
led_pin = machine.Pin(pin_nr, machine.Pin.OUT)
strip = neopixel.NeoPixel(led_pin, num_leds, bpp=3)
max_brightness = int(255 * 0.66)

active_fill = []
add_scale = 20
decr_scale = add_scale/2

#################



# Start a loop to check for updates from the Telegram Bot API
last_update_id = 0

response_data = {
    'chat_id': Ignatius_ID,
    'text': 'Power On'
}
response_url = 'https://api.telegram.org/bot{}/sendMessage'.format(bot_token)
response = urequests.post(response_url, json=response_data)


while True:
    # Construct the URL for the getUpdates API method
    url = 'https://api.telegram.org/bot{}/getUpdates'.format(bot_token)
    if last_update_id != 0:
        url += '?offset={}'.format(last_update_id)

    # Send the request and process the updates
    response = urequests.get(url)
    if response.status_code == 200:
        data = ujson.loads(response.content)
        for update in data['result']:
            handle_update(update)
            last_update_id = update['update_id'] + 1
    time.sleep(0.5)

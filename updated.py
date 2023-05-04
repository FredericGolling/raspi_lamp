import requests
import time


bot_token = '6090202726:AAGSnk8RW3HuZCSTSZITHWyY_swzaBFbyFM'
Ignatius_ID = '1683149821'

while True:
    try:
        response = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates')
        messages = response.json()['result']
        
        for message in messages:
            message_text = message['message']['text']
            message_chat_id = message['message']['chat']['id']
            
            if message_chat_id == Ignatius_ID:
                # Process the message here
                print(f'Received message: {message_text}')
        
        # Wait for 1 second before checking for new messages again
        time.sleep(1)
        
    except Exception as e:
        print(f'Error occurred: {e}')
        # Wait for 5 seconds before trying again
        time.sleep(5)



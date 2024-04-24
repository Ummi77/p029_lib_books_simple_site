


from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 20460272
api_hash = '9e6f44844a41f717e5c035cb0add2984'
client = TelegramClient('anon', api_id, api_hash)

async def downloadMessages():

    # You can print the message history of any chat:
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # # You can download media from messages, too!
        # # The method will return the path where the file was saved.
        # if message.photo:
        #     path = await message.download_media()
        #     print('File saved to', path)  # printed after download is done

with client:
    client.loop.run_until_complete(downloadMessages())
    
    
    
    




if __name__ == '__main__':
    pass



    
    
    
    
    
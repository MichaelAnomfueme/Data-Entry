from dotenv import load_dotenv
import requests
import json
import os
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

data=''
current_article_index = 0
lastmessageid=0

load_dotenv()
API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')

REPLY_MESSAGE = '''
<b>╭  Welcome🙏 to 📰 NewsNerd</b>
<b>├  Get latest update always 🔝 </b>
<b>╰  Press /news to get started</b>
⟬⟬=================================⟭⟭
<b> List of Category supported</b>
╭ /news - all news
├ /national - national news
├ /business - business news
├ /sports - sports news
├ /world - world news
├ /politics - politics news
├ /technology - technology news
├ /startup - startup news
├ /entertainment - entertainment news  
├ /miscellaneous - miscellaneous news
├ /science - science news
╰ /automobile - automobile news
⟬⟬=================================⟭⟭
    ██<b> 🌐Powered by NewsNerd🌐 </b>██
⟬⟬=================================⟭⟭
'''

app = Client('my_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_news(category):
    JSON_URL = f'https://newsnerd.vpms.xyz/news?category={category}'
    response = requests.get(JSON_URL)
    data = json.loads(response.content)['data']
    return data


@app.on_message(filters.command(["start"]))
def handle_news_command(client, message):
    keyboard = [[InlineKeyboardButton("Chaoose Category", callback_data="category")]]
    app.send_video(
                    message.chat.id,
                    'https://i.imgur.com/pb33eZ7.gif',
                    caption=REPLY_MESSAGE,
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
@app.on_callback_query(filters.regex("category"))
def handle_next_button_callback(client, callback_query):
    message_text = '''
⟬⟬=================================⟭⟭
<b> List of Category supported</b>
╭ /news - all news
├ /national - national news
├ /business - business news
├ /sports - sports news
├ /world - world news
├ /politics - politics news
├ /technology - technology news
├ /startup - startup news
├ /entertainment - entertainment news  
├ /miscellaneous - miscellaneous news
├ /science - science news
╰ /automobile - automobile news
⟬⟬=================================⟭⟭
    '''
    client.send_message(callback_query.message.chat.id, message_text, parse_mode=enums.ParseMode.HTML)

# Define a handler for the /news command
@app.on_message(filters.command(["news","national", "business", "sports", "world", "politics", "technology", "startup", "entertainment", "miscellaneous", "science", "automobile"]))
def handle_news_command(client, message):
    global current_article_index
    global data
    if message.text[1:]=='news':
        data=get_news('all')
    else:
        data=get_news(message.text[1:])

    # Get the current article
    article = data[current_article_index]
    title = article['title']
    content = article['content']
    image_url = article['imageUrl']
    
    # Send the article as a message to the Telegram chat
    message_text = f'<b>{title}</b>\n\n{content}\n\nPress the "Next" button to read the next article. \n\n'+'''
⟬⟬==========================⟭⟭
<b>🌐Powered by NewsNerd🌐</b>
⟬⟬==========================⟭⟭
    '''

    keyboard = [[InlineKeyboardButton("Next", callback_data="next")],[InlineKeyboardButton("Chaoose Category", callback_data="category")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    client.send_photo(message.chat.id, image_url, caption=message_text, parse_mode=enums.ParseMode.HTML, reply_markup=reply_markup)

        

# Define a handler for the "Next" button callback
@app.on_callback_query(filters.regex("next"))
def handle_next_button_callback(client, callback_query):
    global current_article_index
    # Increment the current article index
    current_article_index += 1
    # If we've reached the end of the articles list, reset the index
    if current_article_index >= len(data):
        current_article_index = 0
    
    # Get the next article
    article = data[current_article_index]
    title = article['title']
    content = article['content']
    image_url = article['imageUrl']
    
    # Edit the message with the new article
    message_text = f'<b>{title}</b>\n\n{content}\n\nPress the "Next" button to read the next article. \n\n'+'''
⟬⟬==========================⟭⟭
<b>🌐Powered by NewsNerd🌐</b>
⟬⟬==========================⟭⟭
'''
    
    keyboard = [[InlineKeyboardButton("Next", callback_data="next")],[InlineKeyboardButton("Chaoose Category", callback_data="category")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    callback_query.edit_message_media(InputMediaPhoto(image_url, caption=message_text, parse_mode=enums.ParseMode.HTML), reply_markup=reply_markup)

# bot start
app.run()

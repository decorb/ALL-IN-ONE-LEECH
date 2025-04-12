import os
import telegram
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up your bot's token and channel ID
TOKEN = 'your-telegram-bot-token'
CHANNEL_ID = '@your_channel_id'  # Replace with your channel ID

bot = telegram.Bot(token=TOKEN)

def start(update, context):
    """Handle /start command"""
    update.message.reply_text("Hello! I am your leech bot. Send me the link to a lecture or PDF to download.")

def download_file(url):
    """Function to download the file from a URL"""
    response = requests.get(url, stream=True)
    filename = url.split('/')[-1]
    
    # Save file to disk
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return filename

def upload_to_channel(filename):
    """Upload the downloaded file to the Telegram channel"""
    with open(filename, 'rb') as f:
        bot.send_document(chat_id=CHANNEL_ID, document=f)
    os.remove(filename)  # Clean up the downloaded file after uploading

def handle_message(update, context):
    """Handle incoming messages containing URLs"""
    if update.message.text:
        url = update.message.text.strip()
        try:
            filename = download_file(url)
            update.message.reply_text(f"Downloading file from: {url}")
            upload_to_channel(filename)
            update.message.reply_text(f"File successfully uploaded to {CHANNEL_ID}")
        except Exception as e:
            update.message.reply_text(f"An error occurred: {e}")

def main():
    """Set up the Telegram bot and handlers"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))

    # Message handler for any text message
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

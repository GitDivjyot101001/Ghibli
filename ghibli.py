from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import os

API_KEY = "key-1R8R3dLwahM2e996oSMVjhIsdbKDBfvea5vvEoG7Q1WTtMlUOAR77C7O2quSyAIH8lf7Wjwoop0O3fMgbZZUflO2x9FntSqa"  # Replace with your Getimg.ai API key
API_URL = "https://api.getimg.ai/v1/image-to-image"
BOT_TOKEN = "7634486480:AAGhDHTZksZZ9nMxDND1B_zVdtPYVnDpVlg"  # Replace with your Telegram bot token

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a photo, and I'll convert it into Ghibli-style anime!")

def convert_image(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo = update.message.photo[-1]  # Get the highest-resolution photo
    file = context.bot.get_file(photo.file_id)
    file_path = f"photo_{user.id}.jpg"
    file.download(file_path)

    with open(file_path, "rb") as image_file:
        data = {
            "prompt": "Studio Ghibli anime style",
            "negative_prompt": "blurry, distorted, low quality",
            "model": "ghibli-diffusion",
            "cfg_scale": 7,
            "steps": 30
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, json=data, headers=headers)
        result = response.json()

        if "image" in result:
            image_url = result["image"]
            update.message.reply_text(f"Here is your Ghibli-style image: {image_url}")
        else:
            update.message.reply_text("Something went wrong, please try again.")

        os.remove(file_path)  # Clean up local file

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
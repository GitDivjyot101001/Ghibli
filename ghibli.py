import requests
import asyncio
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackContext
)

# Paste your actual keys here
API_KEY = "key-1R8R3dLwahM2e996oSMVjhIsdbKDBfvea5vvEoG7Q1WTtMlUOAR77C7O2quSyAIH8lf7Wjwoop0O3fMgbZZUflO2x9FntSqa"
BOT_TOKEN = "7634486480:AAGhDHTZksZZ9nMxDND1B_zVdtPYVnDpVlg"
API_URL = "https://api.getimg.ai/v1/image-to-image"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Send me a photo, and I'll convert it into Ghibli-style anime!")

async def convert_image(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]  
    file = await context.bot.get_file(photo.file_id)
    file_path = "input_image.jpg"
    await file.download_to_drive(file_path)

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
        await update.message.reply_text(f"Here is your Ghibli-style image: {image_url}")
    else:
        await update.message.reply_text("Something went wrong, please try again.")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, convert_image))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
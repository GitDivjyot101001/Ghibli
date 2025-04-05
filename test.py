import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from PIL import Image
from io import BytesIO
import torch
from diffusers import StableDiffusionImg2ImgPipeline

# === CONFIG ===
TOKEN = "7634486480:AAGhDHTZksZZ9nMxDND1B_zVdtPYVnDpVlg"  # Replace with your Telegram bot token
MODEL_ID = "nitrosocke/Ghibli-Diffusion"

# === LOAD MODEL ===
print("Loading Ghibli model...")
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe.to(device)
pipe.enable_attention_slicing()
print("Model loaded!")


# === IMAGE GENERATION FUNCTION ===
def generate_ghibli_image(input_image, strength):
    input_image = input_image.convert("RGB").resize((512, 512))
    prompt = "Ghibli-style anime painting, soft pastel colors, highly detailed, masterpiece"
    with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
        result = pipe(prompt=prompt, image=input_image, strength=strength).images[0]
    return result


# === BOT COMMANDS ===
def start(update, context):
    update.message.reply_text(
        "Hi! Send me a photo and I'll turn it into a Ghibli-style masterpiece!\n"
        "You can also use `/strength 0.6` to adjust the effect strength (range: 0.3 to 0.8)."
    )

def set_strength(update, context):
    try:
        strength = float(context.args[0])
        strength = max(0.3, min(0.8, strength))
        context.user_data['strength'] = strength
        update.message.reply_text(f"Stylization strength set to {strength}")
    except:
        update.message.reply_text("Please provide a valid number between 0.3 and 0.8")


# === HANDLE PHOTO ===
def handle_image(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO)
    strength = context.user_data.get("strength", 0.6)

    photo_file = update.message.photo[-1].get_file()
    img_bytes = photo_file.download_as_bytearray()
    image = Image.open(BytesIO(img_bytes))

    update.message.reply_text("Processing your image into Ghibli style...")

    try:
        result = generate_ghibli_image(image, strength)
        bio = BytesIO()
        bio.name = "ghibli_result.png"
        result.save(bio, "PNG")
        bio.seek(0)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=bio, caption="Here is your Ghibli-style image!")
    except Exception as e:
        update.message.reply_text("Oops! Something went wrong while processing the image.")


# === MAIN FUNCTION ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("strength", set_strength))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))

    updater.start_polling()
    print("Bot is now running... Press Ctrl+C to stop.")
    updater.idle()


if __name__ == '__main__':
    main()
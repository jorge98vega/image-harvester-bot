import os
import csv
import logging
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, CallbackContext

# Bot token
from bot_token import BOT_TOKEN

# Image storage directory
IMAGE_DIRECTORY = 'images/'

# CSV file to register the received images
CSV_FILE = 'received_images.csv'

# Time limit before sending another image
TIME_RESTRICTION = timedelta(hours=1)

# Blocked users list
BLACKLIST_FILE = 'blacklist.txt'
BLOCKED_USERS = []

# Logging configuration
logging.basicConfig(filename='bot.log', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')

# Logging filter to avoid registering specific messages
class ExcludeHTTPRequests(logging.Filter):
    def filter(self, record):
        return "HTTP Request: POST" not in record.getMessage() and "HTTP Request: GET" not in record.getMessage()

# Add the filter to the logging handlers
logger = logging.getLogger()
for handler in logger.handlers:
    handler.addFilter(ExcludeHTTPRequests())


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 ¡Hola! Soy un bot para recibir imágenes. Puedes enviarme una imagen cada hora.")
    # "👋 Hi! I am a bot designed to received images. You can sent me one image every hour."


async def receive_image(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Check if the user is blocked
    if str(user_id) in BLOCKED_USERS:
        logging.info(f"El usuario bloqueado {user_id} intento enviar una imagen")
        # "The blocked user {user_id} tried to sent an image"
        await update.message.reply_text("⛔ Lo siento, ya no puedes enviar más imágenes a este bot.")
        # "⛔ I'm sorry, but you can no longer send more images to this bot."
    else:
        # Check if the user has already sent an image within the time limit
        if not image_received_within(user_id, TIME_RESTRICTION):
            file_id = update.message.photo[-1].file_id
            file_path = os.path.join(IMAGE_DIRECTORY, f'{user_id}_{file_id}.jpg')
            image = await context.bot.get_file(file_id)
            await image.download_to_drive(custom_path=file_path)

            # Register the received image in the CSV file
            received_time = datetime.now()
            record_received_image(user_id, file_id, received_time)

            await update.message.reply_text("✅ ¡Imagen recibida con éxito!")
            # "✅ Image received succesfully!"
        else:
            await update.message.reply_text("🕐 Debes esperar 1 hora desde la última imagen enviada para enviar una imagen nueva.")
            # "🕐 You must wait one hour from the last sent image to send a new image."


def image_received_within(user_id, time_restriction):
    # Verify if the user has already sent an image within the time limit

    # Read the CSV file to verify the last received image
    with open(CSV_FILE, 'r') as csvfile:
        csv_reader = list(csv.reader(csvfile))

        for row in reversed(csv_reader):
            if row[0] == str(user_id):
                received_time = datetime.fromisoformat(row[2])
                cutoff_time = datetime.now() - time_restriction
                return received_time > cutoff_time
    return False


def record_received_image(user_id, file_id, received_time):
    # Register the received image in the CSV file
    with open(CSV_FILE, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([user_id, file_id, received_time.isoformat()])


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handler
    application.add_handler(CommandHandler("start", start))

    # Receive image handler
    application.add_handler(MessageHandler(filters.PHOTO, receive_image))

    # Configuration
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)

    if not os.path.exists(CSV_FILE):
        # Create the CSV file if it does not exist
        with open(CSV_FILE, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['user_id', 'file_id', 'received_time'])

    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, 'r') as blacklist:
            BLOCKED_USERS.extend(blacklist.read().splitlines())

    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

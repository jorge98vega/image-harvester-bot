# Image Harvester Bot

This repository contains the code for a Telegram bot designed to receive images from users and store them on the machine where the bot is running.

## Features:

1. **Image Reception:** The bot is configured to accept images sent by users through Telegram.

2. **Storage:** Received images are stored locally on the machine where the bot is running.

3. **Rate Limiting:** To avoid storage overflow, users are required to wait for a certain period before sending another image.

4. **User Blocking:** Admins have the ability to block users from sending images. This can be useful for managing inappropriate content or controlling the bot's usage.

## Getting Started:

### Prerequisites:

- Python 3.x
- Python-telegram-bot library (install using `pip install python-telegram-bot`)
You can create a conda environment using `conda create --name <env> --file conda_env.txt`

### Setup:

1. **Telegram Bot Token:**
    - Create a new Telegram bot using the [BotFather](https://t.me/botfather).
    - Obtain the bot token.

2. **Configuration:**
    - Insert your Telegram bot token in a variable named `BOT_TOKEN` in the `bot_token.py` file.
    - Optionally, customize other settings such as the storage path in the `main.py`.

3. **Run the Bot:**
    - Execute the `main.py` script to start the bot.
    - The bot is now ready to receive and store images.

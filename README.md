# YamBot

YamBot is a versatile Telegram bot designed to help users create and manage special messages that others can comment on. It provides a user-friendly interface for creating messages, adding comments, viewing created messages, and more.

Complete documentation can be found on my [blog guide](https://pallontan.wixsite.com/pallon/post/yambot-my-first-telegram-bot).

## Features

- **Create Special Messages**: Users can create unique messages that others can comment on.
- **Add Comments**: Users can add comments to existing special messages.
- **View Messages**: Users can view all special messages they have created.
- **Manage Comments**: Users can see all comments for their created messages.
- **Delete Messages**: Users can delete their own special messages if needed.
- **Inline Query Support**: Users can share and reply to messages using inline queries.

## Requirements

To run YamBot, you'll need:

1. **Telegram Bot Token**: Obtain a Telegram Bot API token from the [Telegram BotFather](https://core.telegram.org/bots#6-botfather). Once you have the token, create a `config.py` file in the root directory of the project and add the token as follows:

    ```python
    TOKEN = "your_telegram_bot_token"
    ```

    Replace `"your_telegram_bot_token"` with your actual Telegram bot token.

2. **Environment Setup**: Ensure that you have a Python environment set up with all the required libraries installed. 

## Usage

Once you've obtained a Telegram bot token and set up your environment, you can start YamBot by running the main script:

```bash
python bot.py

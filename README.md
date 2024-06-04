# YamBot

YamBot is a Telegram bot.

## Requirements

To run YamBot, you'll need:

1. **Telegram Bot Token**: Obtain a Telegram Bot API token from the [Telegram BotFather](https://core.telegram.org/bots#6-botfather). Once you have the token, create a `config.py` file in the root directory of the project and add the token as follows:

    ```python
    TOKEN = "your_telegram_bot_token"
    ```

    Replace `"your_telegram_bot_token"` with your actual Telegram bot token.

2. **Environment Setup**: Ensure that you have a Python environment set up with all the required libraries installed. You can install these libraries using pip:

    ```bash
    pip install -r requirements.txt
    ```

    Note: The `requirements.txt` file contains a list of Python libraries required by YamBot. These libraries are not included in the repository to keep it lightweight. Make sure to install them in your environment before running the bot.

## Usage

Once you've obtained a Telegram bot token and set up your environment, you can start YamBot by running the main script:

```bash
python bot.py

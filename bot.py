import logging
import sqlite3
from config import TOKEN
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, conn, c) -> None:
    """Handle incoming messages and comments."""
    message = update.message.text
    if update.message.reply_to_message:
        # This is a comment
        original_message_id = update.message.reply_to_message.message_id
        c.execute('INSERT INTO comments (message_id, comment) VALUES (?, ?)', 
                  (original_message_id, message))
        conn.commit()
        await update.message.reply_text('Your comment has been saved.')
    else:
        # This is an original message
        message_id = update.message.message_id
        c.execute('INSERT INTO comments (message_id, original_message) VALUES (?, ?)', 
                  (message_id, message))
        conn.commit()
        await update.message.reply_text('Your message has been received. Others can reply to this message to comment.')

# Set up logger
def setup_logger():
    """Set up logging."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        level=logging.INFO
    )
    # Set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logging.getLogger(__name__)

# Set up database connection
def setup_database():
    """Set up the database connection and create the comments table if it does not exist."""
    conn = sqlite3.connect('comments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER,
            original_message TEXT,
            comment TEXT
        )
    ''')
    conn.commit()
    return conn, c

# Main function
def main() -> None:
    """Start the bot."""
    # Set up logging
    logger = setup_logger()

    # Set up database
    conn, c = setup_database()

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # On non-command i.e., message - handle the message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                           lambda update, context: handle_message(update, context, conn, c)))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

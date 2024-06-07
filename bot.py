import logging
import sqlite3
from config import TOKEN
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    logger.info("Received /start command")
    keyboard = [
        [InlineKeyboardButton("Create", callback_data="create")],
        [InlineKeyboardButton("Comment", callback_data="comment")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)
    logger.info("Sent start command reply with options")

async def create_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /create command."""
    logger.info("Received /create command")
    original_message = update.message.text[8:]  # Remove the '/create ' part

    if original_message:
        chat_id = update.effective_chat.id
        message_id = update.message.message_id

        logger.info(f"Creating new special message: {original_message} in chat ID: {chat_id}")

        # Create a unique identifier for the special message
        unique_id = f"{chat_id}-{message_id}"

        # Store the special message in the database
        try:
            c.execute('INSERT INTO comments (unique_id, original_message) VALUES (?, ?)',
                      (unique_id, original_message))
            conn.commit()
            logger.info(f"Stored special message with ID: {unique_id}")
        except Exception as e:
            logger.error(f"Failed to store special message: {e}")
            await update.message.reply_text("Failed to create special message.")
            return

        # Create inline keyboard buttons
        reply_button = InlineKeyboardButton("Reply", url=f"https://t.me/yam_fm_bot")
        share_button = InlineKeyboardButton("Share", switch_inline_query=unique_id)
        reply_markup = InlineKeyboardMarkup([[reply_button, share_button]])
        
        # Send the special message with the inline keyboard button and unique ID
        message_text = f"Special Message ID: {unique_id}\n{original_message}"
        await update.message.reply_text(message_text, reply_markup=reply_markup)
        logger.info(f"Sent special message with ID: {unique_id}")
    else:
        await update.message.reply_text("Please provide a non-empty description for the special message.")
        logger.warning("Received empty original message for /create command")

async def comment_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /comment command."""
    logger.info("Received /comment command")
    message_text = update.message.text[9:]  # Remove the '/comment ' part

    # Split the message text into unique_id and comment_text
    parts = message_text.split(maxsplit=1)
    if len(parts) == 2:
        unique_id, comment_text = parts

        # Check if the special message exists in the database
        c.execute('SELECT original_message, comment FROM comments WHERE unique_id = ?', (unique_id,))
        result = c.fetchone()
        if result:
            original_message, existing_comment = result
            logger.info(f"Found special message with ID: {unique_id}")

            # Append the new comment to the existing comment
            new_comment = f"{existing_comment}\n{comment_text}" if existing_comment else comment_text

            # Update the comment field in the database
            c.execute('UPDATE comments SET comment = ? WHERE unique_id = ?', (new_comment, unique_id))
            conn.commit()
            logger.info(f"Updated comment for special message with ID: {unique_id}")

            await update.message.reply_text(f"Your new comment on '{original_message}':\n{comment_text}")
        else:
            logger.warning(f"Invalid special message ID: {unique_id}")
            await update.message.reply_text("Invalid special message ID. Please provide a valid ID.")
    else:
        logger.warning("Invalid command format for /comment command")
        await update.message.reply_text("Invalid command format. Use /comment <unique_id> <comment_text>")

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages."""
    if update.message:
        logger.info(f"Received regular message: {update.message.text}")
        await update.message.reply_text("This is a regular message.")
    else:
        logger.info(f"User edited a message: {update.edited_message.text}")
        await update.edited_message.reply_text("Notice that you may have edited a message recently, it won't affect anything on me. Please make a command in a new message.")

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
            unique_id TEXT,
            original_message TEXT,
            comment TEXT
        )
    ''')
    conn.commit()
    return conn, c

# Set up logging
logger = setup_logger()

# Set up database
conn, c = setup_database()

# Main function
def main() -> None:
    """Start the bot."""
    logger.info("Starting the bot")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("create", create_command))
    application.add_handler(CommandHandler("comment", comment_command))

    # On non-command i.e., message - handle the message
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot is running")

if __name__ == "__main__":
    main()

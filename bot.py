import os
import logging
import asyncio
import json
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import ollama

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL = os.getenv("OLLAMA_MODEL", "gemma3")
KEEP_ALIVE = os.getenv("KEEP_ALIVE", "-1")
CONTEXT_WINDOW = os.getenv("CONTEXT_WINDOW", "2048")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))
HISTORY_FILE = "chat_history.json"

# Parse variables
try:
    KEEP_ALIVE_VAL = int(KEEP_ALIVE)
except ValueError:
    KEEP_ALIVE_VAL = KEEP_ALIVE

try:
    CONTEXT_WINDOW_VAL = int(CONTEXT_WINDOW)
except ValueError:
    CONTEXT_WINDOW_VAL = 2048

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_chat_history(chat_id):
    """Loads chat history for a specific chat_id."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                return history.get(str(chat_id), [])
        except Exception as e:
            logging.error(f"Error reading history: {e}")
    return []

def save_chat_history(chat_id, history):
    """Saves chat history for a specific chat_id, capping it at MAX_HISTORY."""
    all_histories = {}
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                all_histories = json.load(f)
        except Exception:
            pass
    
    # Cap history
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    
    all_histories[str(chat_id)] = history
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(all_histories, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving history: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message when the command /start is issued."""
    await update.message.reply_text(
        f"Powered by -- Ollama {MODEL} --"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles incoming text messages and queries Ollama."""
    user_message = update.message.text
    
    if not user_message:
        return

    chat_id = update.effective_chat.id
    history = get_chat_history(chat_id)
    
    # Add user message to history
    history.append({'role': 'user', 'content': user_message})

    # Show typing status
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    try:
        # Query Ollama with history
        client = ollama.AsyncClient()
        response = await client.chat(
            model=MODEL,
            messages=history,
            keep_alive=KEEP_ALIVE_VAL,
            options={'num_ctx': CONTEXT_WINDOW_VAL}
        )
        
        bot_response = response['message']['content']
        
        # Add bot response to history and save
        history.append({'role': 'assistant', 'content': bot_response})
        save_chat_history(chat_id, history)
        
        # Send response back to user
        await update.message.reply_text(bot_response)

    except Exception as e:
        logging.error(f"Error calling Ollama: {e}")
        await update.message.reply_text("Sorry, I encountered an error while processing your request.")


if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables.")
        exit(1)
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    
    # Text messages handler
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    
    print(f"Bot is starting with model: {MODEL}...")
    application.run_polling()

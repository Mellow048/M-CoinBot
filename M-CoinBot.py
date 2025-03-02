import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import sqlite3

# Your bot token from BotFather
import os
TOKEN = os.getenv("TOKEN")

# Set up the database
def setup_database():
    conn = sqlite3.connect("airdrop_game.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    conn = sqlite3.connect("airdrop_game.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, points) VALUES (?, 0)", (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("Welcome to M-CoinBot! Tap /tap to earn points. Check your balance with /balance.")

# Tap command
async def tap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    conn = sqlite3.connect("airdrop_game.db")
    c = conn.cursor()
    c.execute("UPDATE users SET points = points + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    c.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    points = c.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"You tapped! Total points: {points}")

# Balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    conn = sqlite3.connect("airdrop_game.db")
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    points = c.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"Your balance: {points} points")

# Main function to run the bot
def main():
    setup_database()  # Initialize the database

    # Create the Application (replaces Updater)
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("tap", tap))
    application.add_handler(CommandHandler("balance", balance))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()

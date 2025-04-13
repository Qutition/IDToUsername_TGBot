import telebot
import os
from flask import Flask, request

app = Flask(__name__)

bot_token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.first_name + (' ' + message.from_user.last_name if message.from_user.last_name else '')
    response = f"Hello, {full_name}! Your ID is {user_id}."
    if username:
        response += f" Your username is @{username}."
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "Message received!")

@app.before_first_request
def set_webhook():
    webhook_url = os.environ.get('WEBHOOK_URL')
    if webhook_url:
        try:
            bot.remove_webhook()
            bot.set_webhook(url=webhook_url)
            print(f"Webhook set to: {webhook_url}")
        except Exception as e:
            print(f"Failed to set webhook: {e}")
    else:
        print("WEBHOOK_URL not set in environment variables.")

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK"

@app.route('/')
def health_check():
    return "Bot is running!"

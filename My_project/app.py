from flask import Flask, request
import telebot
from bot import bot
import config

app = Flask(__name__)

# Маршрут для получения данных от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=config.WEBHOOK_URL)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

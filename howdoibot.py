from flask import Flask, request
import telepot
import urllib3
import json
from howdoi.howdoi import howdoi
from path import Path
from tinydb import TinyDB, Query

db = TinyDB('messages.json')

config_path = Path(__file__).parent / 'config.json'
info = json.load(open(config_path))

if 'pythonanywhere' in info['URL']:
    proxy_url = "http://proxy.server:3128"
    telepot.api._pools = {
        'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
    }
    telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(
        proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

CERT = 'server.crt'
CERT_KEY = 'server.key'
bot = telepot.Bot('{AUTHORIZATION_TOKEN}'.format(
    **info))
bot.setWebhook(
    "https://{URL}/{SECRET_NUMBER}".format(**info), max_connections=1, certificate=open(CERT, 'rb'))

app = Flask(__name__)
secret = "{SECRET_NUMBER}".format(**info)
context = (CERT, CERT_KEY)

howdoi_args = {
    'num_answers': 1,
    'pos': 1,
    'all': False,
    'color': False,
}

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    app.logger.info(update)
    msg = Query()
    if "message" in update and len(db.search(db.message_id == update['message']['message_id'])) == 0:

        db.insert(update['message'])
        text = update["message"]["text"]
        args = {
            'query': text.split(' ')
        }

        args.update(howdoi_args)
        text = howdoi(args)
        chat_id = update["message"]["chat"]["id"]
        try:
            bot.sendMessage(chat_id, "```\n{}```".format(text), parse_mode='Markdown')

        except telepot.exception.BotWasBlockedError as e:
            app.logger.error(str(e))
    return "OK"


if __name__ == "__main__":
    print(info)
    app.run(port=5000, ssl_context=context, debug=True, host='0.0.0.0')

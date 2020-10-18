from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "The bot is up and running"

def run():
    app.run(host='0.0.0.0', port=80080)

def keep_alive():
    server = Thread(target=run)
    server.start()

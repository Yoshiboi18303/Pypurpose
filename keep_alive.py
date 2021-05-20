# Use this code if you're running your bot on Repl.it, and host your bot using UptimeRobot.

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "pypurpose is working!"

def run():
 app.run(host="0.0.0.0", port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()

import psutil
import subprocess as sp
import time
from main import bot
import telebot
while True:
    try:
        proc = sp.Popen(['python', 'main.py'], shell=True)
        proc.wait()
        time.sleep(3)
    except:
        pass
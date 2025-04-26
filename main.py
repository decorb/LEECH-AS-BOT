from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
import os
import sys
import threading
from pyromod import listen
import requests
import json
import time
from p_bar import progress_bar
from subprocess import getstatusoutput
from aiohttp import ClientSession
import helper
from logger import logging
import asyncio
from config import api_id, api_hash, bot_token, auth_users, sudo_users
import re

# Flask App initialization
app = Flask(__name__)

# Pyrogram bot initialization
bot = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)

@app.route("/start", methods=["POST"])
def start_bot():
    return "Bot started!"

@app.route("/stop", methods=["POST"])
def stop_bot():
    os.execl(sys.executable, sys.executable, *sys.argv)

def run_flask():
    app.run(host="0.0.0.0", port=5000)

def run_bot():
    bot.run()

# Flask server running on a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

@bot.on_message(filters.command(["stop"]))
async def cancel_command(bot: Client, m: Message):
    user_id = m.from_user.id if m.from_user is not None else None
    if user_id not in auth_users and user_id not in sudo_users:
        await m.reply(f"**You Are Not Subscribed To This Bot\nContact - @Mahagoraxyz**", quote=True)
        return
    await m.reply_text("**STOPPED**🛑🛑", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    
    user_id = m.from_user.id if m.from_user is not None else None

    if user_id not in auth_users and user_id not in sudo_users:
        await m.reply(f"**You Are Not Subscribed To This Bot\nContact - @Mahagoraxyz**", quote=True)
        return
        
    editable = await m.reply_text(f"**Hey [{m.from_user.first_name}](tg://user?id={m.from_user.id})\nSend txt file**")
    input: Message = await bot.listen(editable.chat.id)
    if input.document:
        x = await input.download()
        await input.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(x))
        credit = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                links.append(i.split("://", 1))
            os.remove(x)
            
        except:
            await m.reply_text("Invalid file input.🥲")
            os.remove(x)
            return
    else:
        content = input.text
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
   
    await editable.edit(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)

    await editable.edit("**Enter Batch Name or send d for grabbing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0

    await editable.edit("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    await editable.edit("**Enter Your Name or send `de` for use default**")
    input3: Message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    await input3.delete(True)
    if raw_text3 == 'de':
        CR = credit
    else:
        CR = raw_text3

    await editable.edit("**Enter Your PW Woking Token\n\nOtherwise Send No**")
    input4: Message = await bot.listen(editable.chat.id)
    pw_token = input4.text
    await input4.delete(True)

    await editable.edit("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/0633f8b6a6f110d34f044.jpg```\n\nor Send No`")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "No"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(count - 1, len(links)):

            V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
            url = "https://" + V

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            # Additional cases and download logic here (the same as your original script)

            # Downloading and uploading logic...
            # Continue as in your script...

            count += 1

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("🔰Done Boss🔰")

# Start bot in the main thread
bot.run()

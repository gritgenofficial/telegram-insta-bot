import os
import telebot
import requests
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

GROUP_USERNAME = "instavideodownloadbott"
GROUP_NAME = "Insta Video Download"

def get_instagram_video_url(insta_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        api_url = "https://saveig.app/api/ajaxSearch"
        data = f"url={insta_url}"
        response = requests.post(api_url, headers=headers, data=data)
        matches = re.findall(r'href="(https://[^"]+\.mp4[^"]*)"', response.text)
        if matches:
            return matches[0]
    except Exception as e:
        print(f"Error: {e}")
    return None

def is_user_member(chat_id):
    try:
        member = bot.get_chat_member(f"@{GROUP_USERNAME}", chat_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Group check error: {e}")
        return False

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        f"👋 Welcome to Insta Reel Downloader Bot!\n\n"
        f"🚨 Please join our group first:\n"
        f"👉 https://t.me/{GROUP_USERNAME}\n\n"
        f"✅ Then send the Instagram link here.",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id

    if not is_user_member(user_id):
        bot.send_message(
            message.chat.id,
            f"🚫 Please join *{GROUP_NAME}* to use this bot:\n👉 https://t.me/{GROUP_USERNAME}",
            parse_mode="Markdown"
        )
        return

    url = message.text.strip()
    if "instagram.com" in url:
        if "?" in url:
            url = url.split("?")[0]

        bot.send_chat_action(message.chat.id, 'upload_video')
        video_url = get_instagram_video_url(url)
        if video_url:
            bot.send_video(message.chat.id, video_url)
        else:
            bot.send_message(message.chat.id, "❌ Failed to fetch video. Make sure it's a public Instagram reel or post.")
    else:
        bot.send_message(message.chat.id, "✅ Please send a valid Instagram link.")

print("✅ Bot started.")
bot.infinity_polling()

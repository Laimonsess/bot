import telebot
import requests
import time
import urllib
from lxml.html import fromstring
from urllib.parse import urljoin

from bs4 import BeautifulSoup

token = "5293205943:AAFsfkrfqLlRUfFX7Ktr6R7PpqIWhqu5n9Q"
id_channel = "@np_chat_1"
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=['text'])
def commands(message):
    bot.send_message(id_channel, message.text)
    if message.text == "Старт":
        bot.send_message(id_channel, "Hello")
        back_post_id = None
        while True:
            post_text = parser(back_post_id)
            back_post_id = post_text[1]

            if post_text[0] != None:
                bot.send_message(id_channel, post_text[0])
                time.sleep(1800)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши Старт")

def parser(back_post_id):
    URL = "https://habr.com/ru/search/?q=python&target_type=posts&order=date"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    post = soup.find("article", class_="tm-articles-list__item", id=True)
    post_id = post["id"]
    
    if post_id != back_post_id:
        title = post.find("a", class_="tm-article-snippet__title-link").text.strip()
        description = post.find("p", class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
        url = post.find("a", class_="tm-article-snippet__title-link", href=True)["href"]
        
        
        return f"{title}\n\n{description}\n\n habr.ru{url}", post_id
    else:
        return None, post_id

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(id_channel, message.text)

bot.infinity_polling()
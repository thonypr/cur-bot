# -*- coding: utf-8 -*-
import os
import telebot
import requests
import json

token = os.environ['TELEGRAM_TOKEN']
# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
# r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=[u"text"])

def handle_start(message):
    to = message.from_user.id
    text = u'{}'.format(message.text)
    amount = text.split(u' ')[0]
    if type(amount) is float or int:
        try:
            if text.split(u' ').count == 2:
                if has_dollar_names(text):
                    byn = get_byn_amount(amount=amount, currency=u"USD")
                    eur_rate = get_byn_amount(amount=1, currency=u"EUR")
                    eur_amount = round(byn / eur_rate, 2)
                    bot.send_message(to, u"🇺🇸 {0}\n🇧🇾{1}\n🇪🇺{2}".format(amount, byn, eur_amount))
                    print (u"Message to{0}:\n🇺🇸 {1}\n🇧🇾{2}\n🇪🇺{3}".format(to, amount, byn, eur_amount))
                elif has_euro_names(text):
                    byn = get_byn_amount(amount=amount, currency=u"EUR")
                    usd_rate = get_byn_amount(amount=1, currency=u"USD")
                    usd_amount = round(byn / usd_rate, 2)
                    bot.send_message(to, u"🇺🇸 {0}\n🇧🇾{1}\n🇪🇺{2}".format(usd_amount, byn, amount))
                    print (u"Message to{0}:\n🇺🇸 {1}\n🇧🇾{2}\n🇪🇺{3}".format(to, usd_amount, byn, amount))
                else:
                    usd_rate = get_byn_amount(amount=1, currency=u"USD")
                    usd_amount = round(int(amount) / usd_rate, 2)
                    eur_rate = get_byn_amount(amount=1, currency=u"EUR")
                    eur_amount = round(int(amount) / eur_rate, 2)
                    bot.send_message(to, u"🇺🇸 {0}\n🇧🇾{1}\n🇪🇺{2}".format(usd_amount, amount, eur_amount))
                    print (u"Message to{0}:\n🇺🇸 {1}\n🇧🇾{2}\n🇪🇺{3}".format(to, usd_amount, amount, eur_amount))
            else:
                bot.send_message(to, u"Неверный ввод. Введите в формате Число Валюта")
                print (u"Message to{0}:\nНеверный ввод. Введите в формате Число Валюта".format(to))
        except ValueError:
            bot.send_message(to, u"Неверный ввод. Введите в формате Число Валюта")
            print (u"Message to{0}:\nНеверный ввод. Введите в формате Число Валюта".format(to))
    else:
            bot.send_message(to, u"Неверный ввод. Введите в формате Число Валюта")
            print (u"Message to{0}:\nНеверный ввод. Введите в формате Число Валюта".format(to))

def get_byn_amount(currency, amount):

    url = "http://www.nbrb.by/API/ExRates/Rates/{}".format(currency)

    querystring = {"ParamMode": "2"}

    try:
        response = requests.request("GET", url, params=querystring)
        r = json.loads(response.content)
        return round(float(r['Cur_OfficialRate']) * float(amount), 2)
    except BaseException:
        return u"Что-то пошло не так..."
      
def has_dollar_names(message):
    synonyms = [u'доллар', u'бакс', u'dollar', u'$', u'бакинских']
    for synonym in synonyms:
        if message.lower().__contains__(synonym):
            return True
    return False


def has_euro_names(message):
    synonyms = [u'евро', u'еврик', u'euro', u'€']
    for synonym in synonyms:
        if message.lower().__contains__(synonym):
            return True
    return False

bot.polling(none_stop=True, interval=0)

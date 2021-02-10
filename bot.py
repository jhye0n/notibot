#!/usr/bin/python3

import telegram
import json
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

class Main():
    def __init__(self):
        self.token_key = self.token_load()
        self.updater = Updater(self.token_key)
        self.updater.dispatcher.add_handler(CommandHandler('weather', Bot().covid19())
        self.updater.start_polling()
        self.updater.idle()
    
    def token_load(self):
        try:
            with open('./env/token.json') as f:
                tokenkey = json.loads(f.read())
                return tokenkey['token']
        except Exception as e:
            print(e)

class Bot():
    def get_apikey(self):
        try:
            with open('./env/token.json') as f:
                apikey = json.loads(f.read())
                return apikey['servicekey']
        except Exception as e:
            print(e)
        
    def covid19(self, update, context):
        servicekey = self.get_apikey()
        url = "https://api.corona-19.kr/korea/?serviceKey={}".format(servicekey)
        req = requests.get(url)

        data = req.json()
        
        # output

        get_update = data['updateTime']
        get_totalbefore = data['TotalCaseBefore']
        get_totalcase = data['TotalCase']
        checkingCounter = data['checkingCounter']
        checkingPercentage = data['checkingPercentage']
        TodayRecovered = data['TodayRecovered']
        TodayDeath = data['TodayDeath']

        return_msg = get_update + "\n\n" + \
            "국내 확진자 합계 : " + get_totalcase + " 명 / " + "전일 대비 (" + get_totalbefore + " 명 ) " + "\n" \
            "국내 검사중 인원 : " + checkingCounter + " 명 (" + checkingPercentage + " %) " + "\n\n" \
            "금일 완치자 합계 : " + TodayRecovered + " 명 " + "\n" \
            "금일 사망자 합계 : " + TodayDeath + " 명 " + "\n"

        update.message.reply_text(return_msg)
        
    
if __name__ == "__main__":
    Main()
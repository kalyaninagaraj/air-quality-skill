from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.configuration.config import Configuration
from mycroft.util.format import nice_date_time
from datetime import datetime
import requests
import json

lookup = {
    'pollution': 'pm25',
    'p.m. 2.5' : "pm25",
    'p.m. 10' : 'pm10',
    'pm 2.5': 'pm25',
    'pm 10': 'pm10',
    'pm2.5': 'pm25',
    'pm10': 'pm10',
    'ozone' : 'o3',
    'nitrogen dioxide' : 'no2',
    'sulphur dioxide' : 'so2',
    'carbon monoxide' : 'co'
}


class AirQuality(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def waqi_query_and_report(self, city, pollutant):
        if self.settings.get('APIKey') is not None:
            AQIReqs = 'https://api.waqi.info/feed/' + city + '/?token=' +  self.settings.get('APIKey')
            reqAQI = requests.get(AQIReqs)
            aqiObj = json.loads(reqAQI.text)
            if aqiObj['status'] == 'ok':
                try:
                    value = aqiObj['data']['iaqi'][lookup[pollutant]]['v']
                except:
                    self.speak_dialog('pollutant.not.reported', {'pollutant' : pollutant, 'city' : city})
                else:
                    stationStr = aqiObj["data"]["city"]["name"]
                    station = stationStr.split(',')[0] + ',' + stationStr.split(',')[1].split('(')[0]
                    dt = nice_date_time(datetime.strptime(aqiObj["data"]["time"]["s"],"%Y-%m-%d %H:%M:%S"), use_ampm=True)
                    self.speak_dialog('pollutant.level.is', {'pollutant' : pollutant,'city' : city, 'value' : value, 'dt': dt, 'station': station})
            else:
                self.speak_dialog('city.not.reported', {'city':city})
        else:
            self.speak_dialog('APIKey.not.found')


    @intent_handler(IntentBuilder('HowPolluted').one_of('How','What')
                    .one_of('polluted','airquality').optionally('place'))
    def handle_how_polluted(self, message):
        if message.data.get('place') is not None:
            city = message.data.get('place')
        else:
            config = Configuration.get()
            city = config['location']['city']['name']
        pollutant = 'pm 2.5'
        self.waqi_query_and_report(city, pollutant)

    @intent_handler(IntentBuilder('WhatIsPollutantLevel').require('pollutant')
                    .optionally('place'))
    def handle_what_is_pollutant_level(self, message):
        if message.data.get('place') is not None:
            city = message.data.get('place')
        else:
            config = Configuration.get()
            city = config['location']['city']['name']
        try:
            pollutant = message.data.get('pollutant')
        except:
            pollutant =  'pm 2.5'
        self.waqi_query_and_report(city, pollutant)

    def stop(self):
        pass


def create_skill():
    return AirQuality()


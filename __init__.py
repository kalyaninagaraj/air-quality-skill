"""
About
-----
Mycroft reports real-time pollutant levels in your city.

Author
------
Kalyani Nagaraj
Dec 2019
"""

from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.configuration.config import Configuration
from mycroft.util.time import now_utc, to_utc
from datetime import datetime
import requests
import json

lookup = {
    'pm 2.5' : 'pm25',
    'pm 10'  : 'pm10',
    'pm2.5'    : 'pm25',
    'pm10'     : 'pm10',
    'pm 10'    : 'pm10',
    'fine particle matter'   : 'pm25',
    'particle pollution'     : 'pm25',
    'pollution': 'pm25',
    'pollutant': 'pm25',
    'nitrogen dioxide' : 'no2',
    'sulphur dioxide'  : 'so2',
    'carbon monoxide'  : 'co'
}

nice_name = {
    'pm2.5'  : 'pm 2.5',
    'pm 2.5' : 'pm 2.5',
    'pm10'   : 'pm 10',
    'pm 10'  : 'pm 10',
    'fine particle matter'   : 'pm 2.5',
    'particle pollution'     : 'pm 2.5',
    'pollution' : 'pm 2.5',
    'pollutant' : 'pm 2.5',
    'nitrogen dioxide' : 'nitrogen dioxide',
    'sulphur dioxide'  : 'sulphur dioxide',
    'carbon monoxide'  : 'carbon monoxide'
}


class AirQuality(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    # Access and report data from the World Air Quality Index project
    def waqi_query_and_report(self, city, pollutant):
        if self.settings.get('APIKey') is not None:
            reqAQI = requests.get('https://api.waqi.info/feed/' + city + '/?token=' +  self.settings.get('APIKey'))
            objAQI = json.loads(reqAQI.text)
            if objAQI['status'] == 'ok':
                try:
                    value = objAQI['data']['iaqi'][lookup[pollutant]]['v']
                except:
                    self.speak_dialog('pollutant.not.reported', {'pollutant' : nice_name[pollutant], 'city' : city})
                else:
                    config = Configuration.get()
                    station_string = objAQI["data"]["city"]["name"]
                    station = station_string.split(',')[0].split('(')[0]
                    utc_time = now_utc() # alternatively, set utc_time to datetime.now(timezone.utc)
                    rec_time = datetime.strptime(objAQI["data"]["time"]["s"] + objAQI["data"]["time"]["tz"].split(':')[0] + objAQI["data"]["time"]["tz"].split(':')[1],"%Y-%m-%d %H:%M:%S%z")
                    rec_time = to_utc(rec_time)
                    timediff = (utc_time - rec_time).total_seconds()
                    if timediff//3600 >= 3: # reading is more than 3 hours old
                        self.dialog('Current readings for this location are not available. Please check back another time.')
                    else:
                        if city in station:
                            incity = ''
                        else:
                           incity = 'in ' + city
                        self.speak_dialog('pollutant.level.is', {'pollutant' : nice_name[pollutant],
                                                                         'incity'    : incity,
                                                                         'value'     : value,
                                                                         'station'   : station})
                    if nice_name[pollutant] == 'pm 2.5':
                        self.health_advisory(value)

            elif objAQI['data'] == 'Unknown station':
                self.speak_dialog('city.not.reported', {'city':city})
            elif objAQI['data'] == 'Invalid key':
                self.speak_dialog('invalid.key', {'city':city})
        else:
            self.speak_dialog('key.not.found')

    # Report a health advisory along with PM2.5 concentration levels
    # http://aqicn.org/scale/
    def health_advisory(self, value):
        if value <= 50:
            self.speak('The air quality is satisfactory, and air pollution poses little or no risk.')
        elif value <= 100:
            self.speak('The air quality is acceptable. There may be a moderate health concern for individuals who are unusually sensitive to air pollution.')
        elif value <= 150:
            self.speak('Members of sensitive groups may experience health effects, but the general public is not likely to be affected.')
        elif value <= 200:
            self.speak('Everyone may begin to experience health effects. Members of sensitive groups may experience more serious health effects.')
        elif value <= 300:
            self.speak('Health alert: everyone may experience more serious health effects.')
        else:
            self.speak('Health warning and emergency conditions: the entire population is more likely to be affected by serious health effects.')


    # Pollutant is not mentioned, PM2.5 implied
    @intent_handler('how.polluted.intent')
    def handle_how_polluted(self, message):
        if message.data.get('place') is not None:
            city = message.data.get('place')
        else:
            config = Configuration.get()
            city = config['location']['city']['name']
        pollutant = 'pm 2.5'
        self.waqi_query_and_report(city, pollutant)


    # Pollutant is mentioned
    @intent_handler('what.is.pollutant.level.intent')
    def handle_what_is_pollutant_level(self, message):
        if message.data.get('pollutant') is not None:
            pollutant = message.data.get('pollutant')
        else:
            pollutant = 'pm 2.5'
        if message.data.get('place') is not None:
            city = message.data.get('place')
        else:
            config = Configuration.get()
            city = config['location']['city']['name']
        self.waqi_query_and_report(city, pollutant)

    def stop(self):
        pass


def create_skill():
    return AirQuality()

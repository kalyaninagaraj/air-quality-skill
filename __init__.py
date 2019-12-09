from mycroft import MycroftSkill, intent_file_handler


class AirQuality(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('quality.air.intent')
    def handle_quality_air(self, message):
        apollutant = ''
        station = ''
        value = ''

        self.speak_dialog('quality.air', data={
            'station': station,
            'value': value,
            'apollutant': apollutant
        })


def create_skill():
    return AirQuality()


from mycroft import MycroftSkill, intent_file_handler


class SonosControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('control.sonos.intent')
    def handle_control_sonos(self, message):
        self.speak_dialog('control.sonos')


def create_skill():
    return SonosControl()


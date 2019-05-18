import soco

from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.util.log import LOG

LOGGER = getLogger(__name__)
VOL_STEP = 5

class SonosControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        speakers = soco.discover()
        if len(speakers) == 0:
            LOGGER.debug("Did not find any Sonos speakers")
            return
        LOGGER.debug("Found Sonos speakers")

        members = {}
        for speaker in speakers:
            members[speaker.player_name.lower()] = speaker

        self.members = members
    # @intent_file_handler('control.sonos.intent')
    # def handle_control_sonos(self, message):
    #     self.speak_dialog('control.sonos')

    @intent_file_handler('play.intent')
    def handle_sonos_play_intent(self, message):
        member = str(message.data.get("speaker"))

        if member == "None":
            LOG.info("Undefined Speaker")
            speaker = self.discovery.any_soco()
        else:
            LOG.info("Defined Speaker")
            speaker = self.members.get(member)

        if speaker == None:
            self.speak_dialog("sonos.nospeaker")
            return
        speaker.play()

        self.speak_dialog("sonos.play")

    @intent_file_handler('pause.intent')
    def handle_sonos_pause_intent(self, message):
        member = str(message.data.get("speaker"))

        if member == "None":
            LOG.info("Undefined Speaker")
            speaker = self.discovery.any_soco()
        else:
            LOG.info("Defined Speaker")
            speaker = self.members.get(member)

        if speaker == None:
            self.speak_dialog("sonos.nospeaker")
            return
        speaker.pause()

        self.speak_dialog("sonos.pause")
            self.speak_dialog("sonos.nospeaker")
            pass

def create_skill():
    return SonosControl()


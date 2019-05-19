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

    @intent_file_handler('play.intent')
    def handle_sonos_play_intent(self, message):
        speaker = get_speaker(message.data.get("speaker"))

        if speaker == None:
            return

        speaker.play()

        self.speak_dialog("sonos.play")

    @intent_file_handler('pause.intent')
    def handle_sonos_pause_intent(self, message):
        speaker = get_speaker(message.data.get("speaker"))

        if speaker == None:
            return

        speaker.pause()

        self.speak_dialog("sonos.pause")


    @intent_file_handler('volume_up.intent')
    def handle_sonos_volume_up_intent(self, message):
        speaker = get_speaker(message.data.get("speaker"))

        if speaker == None:
            return


        speaker.volume = speaker.volume + VOL_STEP
        self.speak_dialog("sonos.volume_up")

    @intent_file_handler('volume_down.intent')
    def handle_sonos_volume_down_intent(self, message):
        speaker = get_speaker(message.data.get("speaker"))

        if speaker == None:
            return


        speaker.volume = speaker.volume - VOL_STEP
        self.speak_dialog("sonos.volume_down")

def get_speaker(utt):
    if utt == None:
        LOG.info("Undefined Speaker")
        speaker = soco.discovery.any_soco()
    else:
        LOG.info("Defined Speaker")
        speaker = SonosControl.members.get(utt)

    if speaker == None:
        SonosControl.speak_dialog("sonos.nospeaker")
        return None

    return speaker

def create_skill():
    return SonosControl()


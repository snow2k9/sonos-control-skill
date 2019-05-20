import soco

from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
# from mycroft.util.parse import extract_number
from mycroft.util.log import getLogger
from mycroft.util.log import LOG

LOGGER = getLogger(__name__)
class SonosControl(MycroftSkill):

    MIN_LEVEL = 0
    DEFAULT_LEVEL = 2
    MAX_LEVEL = 100
    LEVEL_STEP = 10

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        speakers = soco.discover()
        if len(speakers) == 0:
            LOG.debug("Did not find any Sonos speakers")
            return
        LOG.debug("Found Sonos speakers")

    @intent_handler(IntentBuilder("SonosPlay").require("Sonos").require(
        "Play"))
    def handle_sonos_play(self, message):
        speaker = self.__get_speaker(message)
        speaker.play()
        self.speak_dialog('sonos.play')

    @intent_handler(IntentBuilder("SonosPause").require("Sonos").require(
        "Pause"))
    def handle_sonos_pause(self, message):
        speaker = self.__get_speaker(message)
        speaker.pause()
        self.speak_dialog('sonos.pause')


    @intent_handler(IntentBuilder("NextTrack").require("Sonos").require(
        "Next").optionally("Track"))
    def handle_next_track(self, message):
        speaker = self.__get_speaker(message)
        speaker.next()
        self.speak_dialog('track.next')

    @intent_handler(IntentBuilder("PreviousTrack").require("Sonos").require(
        "Previous").optionally("Track"))
    def handle_previous_track(self, message):
        speaker = self.__get_speaker(message)
        speaker.previous()
        self.speak_dialog('track.previous')

    @intent_handler(IntentBuilder("SetVolume").require("Sonos").require(
        "Volume").require("Level").optionally(
        "Increase").optionally("Decrease"))
    def handle_set_volume(self, message):
        speaker = self.__get_speaker(message)
        level = self.__get_volume_level(message)
        self._setvolume(level, speaker)
        self.speak_dialog('set.volume', data={'volume': int(level / 10)})

    def _setvolume(self, vol, speaker):
        speaker.volume = vol


    @staticmethod
    def __bound_level(level):
        if level > SonosControl.MAX_LEVEL:
            level = SonosControl.MAX_LEVEL
        elif level < SonosControl.MIN_LEVEL:
            level = SonosControl.MIN_LEVEL
        return level

    def __get_volume_level(self, message, default=DEFAULT_LEVEL):
        level_str = message.data.get('Level', default)
        level = default

        try:
            level = int(level_str)
        except ValueError:
            pass

        level = self.__bound_level(level)
        level = level * self.LEVEL_STEP
        return level

    def __get_speaker(self, message):
        # TODO: Get Speaker by name
        # TODO: Work with Groups
        speaker = soco.discovery.any_soco()

        return speaker

def create_skill():
    return SonosControl()


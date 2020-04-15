'''This is the speech recognizer module for vaac.'''
import os
from pocketsphinx import LiveSpeech, get_model_path

model_path = "/home/shrinidhi/project/vaac/vaac_model"

class VaacSpeech(LiveSpeech):
    def __init__(self, **kwargs):
        self.recognized_commands = []
        super(VaacSpeech, self).__init__(**kwargs)

    def __iter__(self):
        with self.ad:
            with self.start_utterance():
                while self.ad.readinto(self.buf) >= 0:
                    self.process_raw(self.buf, self.no_search, self.full_utt)
                    if self.keyphrase and self.hyp():
                        with self.end_utterance():
                            self.recognized_commands.append(str(self))
                            yield self

                    elif self.in_speech != self.get_in_speech():
                        self.in_speech = self.get_in_speech()
                        if not self.in_speech and self.hyp():
                            with self.end_utterance():
                                self.recognized_commands.append(str(self))
                                yield self

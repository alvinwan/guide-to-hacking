from AVFoundation import AVSpeechUtterance, AVSpeechSynthesizer
import time


def say(text):
    synth = AVSpeechSynthesizer.alloc().init()  # init speaker
    utterance = AVSpeechUtterance.speechUtteranceWithString_(text)  # init utterance
    synth.speakUtterance_(utterance)  # speak utterance
    time.sleep(3)  # allow time for speaking to finish


if __name__ == '__main__':
    say("I wish oranges came in purple.")
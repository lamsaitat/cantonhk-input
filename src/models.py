__author__ = 'kuro'


IBUS_WEIGHT_MAX = 500   # Assume that we won't hit 500 choices per key


class CantonKey(object):
    key_sequence = None
    choices = []

    def __init__(self, key_sequence, choices=[]):
        self.key_sequence = key_sequence
        self.choices = choices

    def to_ibus(self):
        output = ""
        for character in self.choices:
            output += "%s\t%s\t%s\n" % (self.key_sequence, character, IBUS_WEIGHT_MAX - self.choices.index(character))
        return output
from pynput.keyboard import Key

HARDCODED_SPECIAL_KEYS = {
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "shift": Key.shift,
    "space": Key.space,
}

class Command():
    def __init__(self, keyword: str, key: str, duration: float):
        """
        keyword: the word to trigger the keypress
        key: the key being pressed
        duration: the length to press the key
        """
        self.keyword = keyword
        self.duration = duration

        if key in HARDCODED_SPECIAL_KEYS.keys():
            # if it's one of the special ones
            self.key = HARDCODED_SPECIAL_KEYS[key]
        else:
            self.key = key

    def get_info(self):
        return self.keyword, self.key, self.duration
    
    def mult_duration(self, value: float):
        """
        Use this to multiply any duration - for use in list comprehensions.
        """
        setattr(self, "duration", value)
        return self


class Modifier():
    def __init__(self, keyword: str, duration: float, rate: float):
        """
        Allows you to modify any Command and then run stores that Command in an object.
        """

        self.command = None

        # not needed for this but super cool
        # for attribute, value in attributes_and_values:
        #     setattr(self.command, attribute, value)



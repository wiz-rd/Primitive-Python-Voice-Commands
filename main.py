import json
import threading
from time import sleep

from pynput.keyboard import Controller
from pyaudio import PyAudio, paInt16
from vosk import Model, KaldiRecognizer

from commands import Command

# special thanks to:
# https://stackoverflow.com/questions/51525691/realtime-offline-speech-recognition-in-python

models = {
    "large": "./models/vosk-model-en-us-0.42-gigaspeech",
    "small": "./models/vosk-model-en-us-0.22",
}

RATE = 16000
model = Model(models["large"])
recognizer = KaldiRecognizer(model, RATE)

mic = PyAudio()
stream = mic.open(rate=RATE, channels=1, format=paInt16, input=True, frames_per_buffer=8192)
stream.start_stream()


# should be command
# and then duration
COMMANDS = [
    Command("jump", "space", 0.5),
    Command("right", "right", 0.5),
    Command("left", "left", 0.5),
    Command("run", "shift", 10),
    Command("type", "a", 0.5)
]

MODIFIERS = [
    "long",
    "longer",
    "short",
    "shorter",
    "spam",
    "sequential",
]

# making a list of command keywords
KEYWORDS = [command.keyword for command in COMMANDS]

def make_threads(commands: list[Command], modifiers: list[str]):
    """
    Creates threads for each keypress
    """

    for modifier in modifiers:
        # modifies all commands to follow the given pattern:
        # "long" increases every input by 50%
        # "short" decreases every keypress by 50%
        # and "rapid" is a special one that spams the keys at 15% duration
        if modifier == "long":
            commands = [cmd.mult_duration(2) for cmd in commands]
        elif modifier == "longer":
            commands = [cmd.mult_duration(4) for cmd in commands]
        elif modifier == "short":
            commands = [cmd.mult_duration(0.5) for cmd in commands]
        elif modifier == "shorter":
            commands = [cmd.mult_duration(0.15) for cmd in commands]
        elif modifier == "spam":
            commands = [cmd.mult_duration(0.15) for cmd in commands]
            # making the list of commands a lot longer - 8 times as long
            commands = commands * 8
        elif modifier == "sequential":
            # runs the commands in order and awaits durations
            for command in commands:
                run_command(command)
            return

    for command_to_run in commands:
        # getting the index of the key to press, and as such, the Command
        print(f"running: {command_to_run.keyword}")
        thread = threading.Thread(target=run_command, daemon=True, args=[command_to_run])
        thread.start()


# def make_threads(keys: list):
#     """
#     Creates threads to hold down each key as long as necessary.
#     """

#     for key_to_press in keys:
#         # getting the index of the key to press, and as such, the Command
#         index = KEYWORDS.index(key_to_press)

#         command = COMMANDS[index]

#         print(f"running: {key_to_press}")
#         thread = threading.Thread(target=run_command, daemon=True, args=[])
#         thread.start()


def run_command(key_command: Command):
    cont = Controller()
    
    cont.press(key_command.key)
    sleep(key_command.duration)
    cont.release(key_command.key)

    return


def process_commands(commands: str):
    
    actions = list()
    modifiers = list()

    # for every word in the input
    # make a list

    # this makes a list of strings and relies
    # on make_threads() to parse out the commands
    # for command in KEYWORDS:
    #     if command in commands:
    #         actions.append(command)
    #     else:
    #         continue

    # this makes a list of Command objects
    for command in commands.split(" "):
        if command in KEYWORDS:
            index = KEYWORDS.index(command)
            cmd_obj = COMMANDS[index]
            actions.append(cmd_obj)
        elif command in MODIFIERS:
            modifiers.append(command)
        else:
            print(f"not a command: {command}")
    
    # if there IS a command
    if len(actions) > 0:
        # run all commands from input
        make_threads(actions, modifiers)


while True:
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):
        current_input = json.loads(recognizer.Result())
        current_commands = current_input["text"]
        print(f"{current_input['text']}")

        process_commands(current_commands)

# to do
# for "word" in "words":
#   if word in outputs:
#       merge words to total..?
#   
#   perform total action

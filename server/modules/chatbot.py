from paddlenlp import Taskflow

dialogue=None

def init():
    global dialogue
    if dialogue==None:
        dialogue = Taskflow("dialogue")


def start(text):
    global dialogue
    init()
    data = [text]
    result = dialogue(data)
    return result[0]


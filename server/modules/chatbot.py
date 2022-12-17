import paddlehub as hub

chatbot_model=None

def init():
    global chatbot_model
    if chatbot_model==None:
        chatbot_model = hub.Module(name='plato-mini')


def start(text):
    global chatbot_model
    init()
    data = [[text]]
    result = chatbot_model.predict(data,use_gpu=True) 
    return result[0]


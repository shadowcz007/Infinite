
import paddlehub as hub

module = hub.Module(name='baidu_translate')

def start(t):
    result = module.translate(t)
    return result
import json

def get_config():
    with open("config.json", 'r') as f:
        return json.load(f)


def load_state():
    try:
        with open("state.json", 'r') as f:
            x = json.load(f)
        return x
    except IOError:
        return {}


def save_state(res):
    with open('state.json', 'w') as f:
        json.dump(res, f)
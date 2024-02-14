import json

def get_credentials():
    with open('config.json') as f:
        config = json.load(f)
    return config.get('CREDY_USERNAME'), config.get('CREDY_PASSWORD')

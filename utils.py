import json
import pprint as pp

def read_json(file):
    with open(file, 'r') as opened_file:
        json_obj = json.load(opened_file)
        return json_obj
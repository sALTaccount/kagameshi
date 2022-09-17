import json

responses = {}
try:
    with open('responses.json', 'r', encoding='utf-8') as f:
        responses = json.loads(f.read())
except FileNotFoundError:
    pass

def insert_response(connection, image_id, user_id, response):
    global responses
    responses[int(image_id)] = response
    with open('responses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(responses))

def create_table_if_not_exist(connection):
    pass

def get_responses(connection):
    global responses
    return responses

def get_response(connection, post_id):
    global responses
    try:
        return responses[int(post_id)]
    except KeyError:
        return None

import base64
import time
from pprint import pprint

import requests
import json

filename = '/Users/aymanmoustafa/projects/youtube/ollama-collection/equations_plot.png'

def get_base64(filename):
    with open(filename, 'rb') as f:
        encoded_string = base64.b64encode(f.read()).decode('utf-8')
        return encoded_string

def generate_response(base_url, model_name, user_input, image_64):
    url = f'{base_url}/api/chat'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": model_name,
        "stream": False,
        "messages":[ {
            "role":"user",
            "content":user_input,
            "images":[image_64],
            "stream": False
    }
        ]


    }
    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    end_time = time.time()
    response_time = end_time - start_time  # Calculate response time
    if response.status_code == 200:
        return response, response_time
    else:
        error_message = response.text
        print(error_message)
        return '', response_time

base_64 = get_base64(filename)
base_url = f'http://localhost:11434'
user_input = "describe this image"
response, response_time = generate_response(base_url,'llava:latest', user_input, base_64 )

pprint(response.text)
print(response_time)

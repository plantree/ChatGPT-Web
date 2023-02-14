"""
A simple server for request ChatGPT
"""
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
import requests
from requests.adapters import HTTPAdapter, Retry
import copy
import yaml
import hashlib
import random

############# utils ####################
def generate_response(code, message):
    return jsonify({
        'code': code,
        'msg': message
    })

def parse_yaml(file):
    with open(file, 'r') as f:
        content = f.read()
        config = yaml.load(content, Loader=yaml.FullLoader)
        return config

def encrypt_md5(s):
    md5 = hashlib.md5()
    md5.update((s + G_CONFIG['salt']).encode())
    return md5.hexdigest()

def random_select(keys):
    return keys[random.randint(0, len(keys) - 1)]

########################################

################# config ##############
CHATGPT_API = "https://api.openai.com/v1/completions"

# ref: https://platform.openai.com/docs/api-reference/completions/create
DEFAULT_CONFIG = {
    # ref: https://platform.openai.com/docs/models/gpt-3
    'model': 'text-davinci-003',
    'max_tokens': 4000,
    # deterministic
    'temperature': 0.4
}

G_CONFIG = parse_yaml('./config.yml')
G_CONFIG['encrypted_tokens'] = []
# for token in G_CONFIG['tokens']:
#     G_CONFIG['encrypted_tokens'].append(encrypt_md5(token))
for token in G_CONFIG['tokens']:
    G_CONFIG['encrypted_tokens'].append(token)
#######################################

app = Flask(__name__)
CORS(app, origins=G_CONFIG['origins'])
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=['1000 per day', '100 per hour']
)
session = requests.Session()
retries = Retry(total=G_CONFIG['max_retry'], backoff_factor=0.1)
session.mount(CHATGPT_API, HTTPAdapter(max_retries=retries))

@app.route("/")
def index():
    return 'Hello, ChatGPT'

''''
args
    token
'''
@app.post("/api/chatgpt/login")
@limiter.limit(str(G_CONFIG['limit']) + '/minute')
def login_chatgpt():
    args = request.args
    token = args.get('token')
    if token == None:
        return generate_response(-1001, 'need token to ask')
    else:
        if token not in G_CONFIG['encrypted_tokens']:
            return generate_response(-1002, 'illegal token')
    return generate_response(0, 'success')
        
'''
args:
    prompt
    temperature
    token
'''
@app.post("/api/chatgpt/ask")
@limiter.limit(str(G_CONFIG['limit']) + '/minute')
def request_chatgpt():
    args = request.args
    prompt = args.get('prompt')
    temperature = args.get('temperature')
    token = args.get('token')

    if token == None:
        return generate_response(-1001, 'need token to ask')
    else:
        if token not in G_CONFIG['encrypted_tokens']:
            return generate_response(-1002, 'illegal token')
    if prompt == None:
        return generate_response(-1003, 'need prompt')
    
    # request chatgpt
    config = copy.deepcopy(DEFAULT_CONFIG)
    config['prompt'] = prompt
    if temperature != None:
        config['temperature'] = temperature
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + random_select(G_CONFIG['keys'])
    }
    req = session.post(CHATGPT_API, headers=headers, json=config, timeout=G_CONFIG['timeout'])
    if req.status_code != 200:
        return generate_response(-1004, 'request chatgpt failed. err: ' + req.json()['error']['message'])
    else:
        return generate_response(0, req.json()['choices'][0]['text'])

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=G_CONFIG['port'],
        debug=True)

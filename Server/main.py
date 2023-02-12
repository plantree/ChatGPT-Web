"""
A simple server for request ChatGPT
"""
from flask import Flask, jsonify
from markupsafe import escape
import requests

app = Flask(__name__)

CAHTGPT_API = "https://api.openai.com/v1/completions"

# ref: https://platform.openai.com/docs/api-reference/completions/create
default_config = {
    # ref: https://platform.openai.com/docs/models/gpt-3
    'model': 'text-davinci-003',
    'max_tokens': 4096,
    # deterministic
    'temperature': 0.2
}

@app.get("/api/chatgpt/ask/<parameter>")
def request_chatgpt():
    # get prompt
    prompt = escape(parameter)

    if prompt == '':    
        message = {
            "code": -1,
            "err_msg": "need prompt"
        }
        return jsonify(message)
    # request chatgpt
    config = default_config.copy()
    config["prompt"] = prompt
    req = requests.post(CAHTGPT_API, )

    
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=8000,
        debug=True)

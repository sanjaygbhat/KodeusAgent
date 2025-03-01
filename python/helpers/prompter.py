#!/usr/bin/python3

import sys
import requests
import json

def send(text:str, context="", message_id=""):
    # URL to prompt
    url = "http://localhost:80/message"

    # Create payload
    payload = json.dumps({
        "text": text,
        "context": context,
        "message_id": message_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # Send request
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

def send_async(text, context="924ba640-cca5-434e-814d-fa3062691abd", message_id=""):
    # URL to prompt
    url = "http://localhost:80/message_async"

    # Create payload
    payload = json.dumps({
        "text": text,
        "context": context,
        "message_id": message_id
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # Send request
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

if __name__ == "__main__":
    # When run as a script, use command line arguments
    response = send_async(" ".join(sys.argv[1:]),context="924ba640-cca5-434e-814d-fa3062691abd", message_id="")
    print(response)

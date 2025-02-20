#!/usr/bin/python3

import sys
import requests
import json

# URL to prompt
url = "http://localhost:80/message_async"

# Create payload
payload = json.dumps({
  "text": " ".join(sys.argv[1:]),
  "context": "924ba640-cca5-434e-814d-fa3062691abc",
  "message_id": ""
})
headers = {
  'Content-Type': 'application/json'
}

# Send request
response = requests.request("POST", url, headers=headers, data=payload)

# Print response
print(response.text)

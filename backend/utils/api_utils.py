import requests

def post_to_api(url, payload, headers=None):
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

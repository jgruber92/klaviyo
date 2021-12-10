import klaviyo
import requests


def getList():
    url = "https://a.klaviyo.com/api/v2/lists?api_key=API_KEY"

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)

    print(response.text)

import klaviyo
import requests
import json
import keys

PRIVATE_KEY = keys.PRIVATE_KEY
PUBLIC_KEY = keys.PUBLIC_KEY
PERSON_ID = keys.PERSON_ID
WEATHERSTACK_ACCESS_KEY = keys.WEATHERSTACK_ACCESS_KEY
BASE_URL = "https://a.klaviyo.com/api/"
SEGMENT_ID = "Xw5kWt"

client = klaviyo.Klaviyo(public_token=PUBLIC_KEY, private_token=PRIVATE_KEY)


def identify(email, city):
    url = BASE_URL + "identify"

    payload = (
        '{"token":"'
        + PUBLIC_KEY
        + '","properties":{"$email":"'
        + email
        + '","$city":"'
        + city
        + '"}}'
    )
    headers = {
        "Content-Type": "application/json",
        "cache-control": "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def getSegmentMembers():
    url = BASE_URL + "v2/group/" + SEGMENT_ID + "/members/all?api_key=" + PRIVATE_KEY

    headers = {"cache-control": "no-cache"}
    response = requests.request("GET", url, headers=headers)
    r_dict = response.json()
    print(r_dict)


def trackWeather():
    url = "https://a.klaviyo.com/api/track"

    payload = '{\n  "token": "WjsNyD",\n  "event": "Weather Update",\n  "customer_properties": {\n    "$email": "jefferson.gruber92+boston.com",\n    "precipitation": "Rain"\n  }\n}'
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


def getProfile():
    identity_url = "https://a.klaviyo.com/api/identify"
    identity_payload = {
        "token": "WjsNyD",
        "properties": {"$email": "jefferson.gruber92+austin@gmail.com"},
    }

    identity_Headers = {
        "Accept": "text/html",
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", identity_url, data=identity_payload, headers=identity_Headers
    )

    print(response.text)


def getProfileLocation():
    url = "https://a.klaviyo.com/api/v1/person/01FPJR3P41DPTP84GZ5V90H198"
    querystring = {"api_key": PRIVATE_KEY}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    json_response = response.json
    print(json_response["$city"])

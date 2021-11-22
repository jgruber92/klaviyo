import klaviyo
import requests

PRIVATE_KEY = "pk_34a431d058e507565efb49b1e550cfad3e"
PUBLIC_KEY = "WjsNyD"
PERSON_ID = "01FKPCW7YKWX9Z9SA1XJ3DVGX0"
WEATHERSTACK_ACCESS_KEY = "b3eaec142b46a351692531ce29387c3a"

client = klaviyo.Klaviyo(public_token=PUBLIC_KEY, private_token=PRIVATE_KEY)


def getAllCitiesInList():
    list_members_base_url = "https://a.klaviyo.com/api/v2/group/QVT3Yk/members/all"
    querystring = {"api_key": PRIVATE_KEY}
    headers = {"Accept": "application/json"}
    response = requests.request(
        "GET", list_members_base_url, headers=headers, params=querystring
    )

    print(response.text)


getAllCitiesInList()


def updateProfile(attribute, value):
    client.Profiles.update_profile(PERSON_ID, {attribute: value})


def getProfile():
    url = "https://a.klaviyo.com/api/v1/person/" + PERSON_ID
    querystring = {"api_key": PRIVATE_KEY}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)


def getIdentity():
    identity_url = "https://a.klaviyo.com/api/identify"
    identity_payload = {
        "token": "PUBLIC_KEY",
        "properties": {
            "$email": "abraham.lincoln@klaviyo.com",
            "$first_name": "Abraham",
            "$last_name": "Lincoln",
            "$city": "Springfield",
            "$region": "Illinois",
        },
    }

    identity_Headers = {
        "Accept": "text/html",
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", identity_url, data=identity_payload, headers=identity_Headers
    )

    print(response.status_code)


def list_to_string(s):
    string = ""
    return string.join(s)


def is_it_raining(is_it_raining_location):
    params = {"access_key": WEATHERSTACK_ACCESS_KEY, "query": is_it_raining_location}
    current_weather = requests.get("http://api.weatherstack.com/current", params)
    weather_api_response = current_weather.json()
    weather_list = weather_api_response["current"]["weather_descriptions"]
    weather = list_to_string(weather_list)

    if "Rain" in weather:
        return True

    return False


def getProfileLocation():
    profile_base_url = "https://a.klaviyo.com/api/v1/person/" + PERSON_ID
    querystring = {"api_key": "pk_34a431d058e507565efb49b1e550cfad3e"}
    headers = {"Accept": "application/json"}
    response = requests.request(
        "GET", profile_base_url, headers=headers, params=querystring
    )
    profile_response = response.json()
    value_list = profile_response.get("$city")
    return value_list


def raining_message(message_location):
    message = (
        ("It's raining in" + message_location)
        if is_it_raining(location) == True
        else print("It's not raining in " + location)
    )
    print(message)


updateProfile("city", "Seattle")
location = getProfileLocation()
is_it_raining(location)
raining_message(location)

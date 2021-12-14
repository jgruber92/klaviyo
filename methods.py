import klaviyo
import requests

# I've imported the keys module where I store my access key.
# I've added this to the .gitignore file so they are not public in github
import keys

PRIVATE_KEY = keys.PRIVATE_KEY
PUBLIC_KEY = keys.PUBLIC_KEY
PERSON_ID = keys.PERSON_ID
WEATHERSTACK_ACCESS_KEY = keys.WEATHERSTACK_ACCESS_KEY
BASE_URL = "https://a.klaviyo.com/api/"

# Even though it is bad practice to hardcode this, I only need to use 1 segment which is why it's hardcoded
# right now. In other scenarios where you would be using one of many segments, you
# would want to dynamically choose a segment and it would not longer make sense to hardcode this.
SEGMENT_ID = "Xw5kWt"

client = klaviyo.Klaviyo(public_token=PUBLIC_KEY, private_token=PRIVATE_KEY)

# Creates a new profile - I will use this during the demo manually to represent a new profile
# being created. It's not used in the script though
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


# Returns a list of the locations of all the profiles in a segment
def getSegmentMembersLocation():
    url = BASE_URL + "v2/group/" + SEGMENT_ID + "/members/all?api_key=" + PRIVATE_KEY
    i = 0
    profile_location_list = []

    headers = {"cache-control": "no-cache"}
    response = requests.request("GET", url, headers=headers)

    # Convert response into json and then into a dictionary to easily access resposne data to pull out the locations
    records = response.json()
    r_dict = records["records"]

    # Loops through response and add all the location to a list to be returned
    while i < (len(r_dict)):
        profile_id = r_dict[i].get("id")
        location = getProfileLocation(profile_id)
        profile_location_list.append(location)
        i += 1
        profile_id = ""

    return profile_location_list


# Returns a list of the emails for each member in a segment
def getSegmentMembersEmail():
    url = BASE_URL + "v2/group/" + SEGMENT_ID + "/members/all?api_key=" + PRIVATE_KEY
    i = 0
    profile_email_list = []

    headers = {"cache-control": "no-cache"}
    response = requests.request("GET", url, headers=headers)

    # Convert response into json and then into a dictionary to easily access resposne data to pull out the locations
    records = response.json()
    r_dict = records["records"]

    # Loops through response and adds all the emails to a list to be returned
    while i < (len(r_dict)):
        profile_email = r_dict[i].get("email")
        profile_email_list.append(profile_email)
        i += 1
        profile_email = ""

    return profile_email_list


# Returns the location of a profile
def getProfileLocation(person_id):
    url = BASE_URL + "v1/person/" + person_id + "?api_key=" + PRIVATE_KEY
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)

    # Converts response to json and returns the location as a string
    profile = response.json()
    location = profile["$city"]

    return location


# Basic utility function that converts a list to a string
def listToString(list_to_convert):
    string = "".join(list_to_convert)
    return string


# Returns the current weather for each profile in a segment
def getWeather(city):

    # In the case of getting a weathe forecast, this is where the endpoint would be changed to be "/forecast?access_key={{YOUR_ACCESS_KEY}}& query={{city}}&forecast_days = 3" instead of "current"
    url = "http://api.weatherstack.com/current"

    querystring = {"access_key": WEATHERSTACK_ACCESS_KEY, "query": city}

    payload = ""
    headers = {"cache-control": "no-cache"}

    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    weather_dict = response.json()

    # Returns a list of the current weather in a location
    return listToString(weather_dict["current"]["weather_descriptions"])


# Tracks a weather event for each profile in a segment based on their email
def trackWeatherUpdate(email, location):
    url = "https://a.klaviyo.com/api/track"
    weather = getWeather(location)
    payload = (
        '{"token":"'
        + PUBLIC_KEY
        + '","event":"Weather Update","customer_properties": {"$email":"'
        + email
        + '"},"properties": {"current_weather":"'
        + weather
        + '"}}'
    )
    headers = {
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, data=payload, headers=headers)


# The main script that tracks the weather for all profiles with a location associated
def weatherScript():
    i = 0
    emails = getSegmentMembersEmail()
    locations = getSegmentMembersLocation()

    # Loops through all of the profiles and tracks the current weather for each of them
    while i < len(emails):
        trackWeatherUpdate(emails[i], locations[i])
        i += 1

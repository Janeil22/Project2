import requests
import pandas as pd
import sqlalchemy as db

#root URL to derive events
url = "https://app.ticketmaster.com/discovery/v2/events"

API_KEY = "zWmwA15ShfzkNwMGKQ7Ih2RDbAWaoIvV"

#Event Search Parameters
parameters = {'apikey':API_KEY, 'countryCode':'US', 'classificationName':'music', 'startDateTime':'2022-07-01T14:00:00Z', 'endDateTime': '2022-08-01T14:00:00Z', 'sort':'date,asc', 'city':'', 'stateCode':''}

#Get City name and State Code from user
parameters['city'] = "Las Vegas" #input("Enter City: ")
parameters['stateCode'] = "NV" #input("Enter State Code: ")

#get all events within city
response = requests.get(url, parameters)
response = response.json()
Events = list()
eventName = list()
eventDate = list()
eventVenue = list()

#extract Event Id from json and input in empty list
for event in response:
    for x in (response["_embedded"]["events"]):
        Events.append(x["id"])
        eventName.append(x["name"])
        eventDate.append(x["dates"]["start"]["localDate"])
        eventVenue.append(x["_embedded"]["venues"])

EventDetails = {"Event ID":Events, "Event Name":eventName, "Event Date":eventDate, "Event Venues":eventVenue}

data = pd.DataFrame.from_dict(EventDetails)

'''
print(Events[0])
details = requests.get('https://app.ticketmaster.com/discovery/v2/events/' +Events[0]+ '.json?apikey=zWmwA15ShfzkNwMGKQ7Ih2RDbAWaoIvV', {'locale':'en-us'})
print(details.json())

for event in Events["EventIDs"]:
    details = requests.get(url, {'id':event, 'apikey':API_KEY})
    details = details.json()
    print(details)
    break
    for x in (details["_embedded"]["venues"]):
        Events["location"].append(["name"])
        Events["location"].append(["address"]["line1"])
        Events["location"].append(["city"]["name"])
        Events["location"].append(["state"]["stateCode"])'''
import requests

import pandas as pd

import sqlalchemy as db

# root URL to derive events
url = "https://app.ticketmaster.com/discovery/v2/events"

API_KEY = "zWmwA15ShfzkNwMGKQ7Ih2RDbAWaoIvV"

# Event Search Parameters
parameters = {
  'apikey': API_KEY, 'countryCode': 'US', 'classificationName': 'music',
  'startDateTime': '2022-07-01T14:00:00Z',
  'endDateTime': '2022-08-01T14:00:00Z',
  'sort': 'date,asc', 'city': '', 'stateCode': ''
  }

# Get City name and State Code from user
parameters['city'] = input("Enter City: ")
parameters['stateCode'] = input("Enter State Code: ")

# get all events within city
response = requests.get(url, parameters)
response = response.json()
Events = list()
eventName = list()
eventDate = list()
VenueName = list()
VenueAddy = list()

# extract Event Id from json and input in empty list
for event in response:
    for x in (response["_embedded"]["events"]):
        Events.append(x["id"])
        eventName.append(x["name"])
        eventDate.append(x["dates"]["start"]["localDate"])
        for ven in (x["_embedded"]["venues"]):
            VenueName.append(ven["name"])
            VenueAddy.append(ven["address"]["line1"])

EventDetails = {"Event ID": Events, "Event Name": eventName,
                "Event Date": eventDate, "Venue Name": VenueName,
                "Venue Address": VenueAddy}

# creates and prints out a database


def create_database(info, db_name, table_name):
    data = pd.DataFrame.from_dict(info)
    engine = db.create_engine('sqlite:///' + db_name + '.db')
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM "+table_name+";").fetchall()
    print(pd.DataFrame(query_result), "\n")


create_database(EventDetails, "EVENTS", "Details")

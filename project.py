import requests

import pandas as pd

import sqlalchemy as db

import sys

import os

# root URL to derive events
url = "https://app.ticketmaster.com/discovery/v2/events"

# Event Search Parameters
parameters = {
  'apikey': os.environ.get('TICKETMASTER_API_KEY'), 'countryCode': 'US',
  'classificationName': 'music', 'startDateTime': '2022-07-05T14:00:00Z',
  'endDateTime': '2022-08-05T14:00:00Z',
  'sort': 'date,asc', 'city': '', 'stateCode': ''
  }

# lists to hold event details
eventId = list()
eventName = list()
eventDate = list()
VenueName = list()
VenueAddy = list()


# Function to get City name
def get_city():
    city = input("Enter City: ")
    return city


# Function to get State name
def get_state():
    state = input("Enter State Code: ")
    return state


# function to create a dictionary with parameters are values
def get_dict(id, name, date, venue, address):
    dct = {
        "Event ID": id, "Event Name": name,
        "Event Date": date, "Venue Name": venue,
        "Venue Address": address
        }
    return dct


# fuctions to extract Event details from json and input in empty lists
def extractor(resp):
    for event in resp:
        try:
            for x in (resp["_embedded"]["events"]):
                eventId.append(x["id"])
                eventName.append(x["name"])
                eventDate.append(x["dates"]["start"]["localDate"])
                for ven in (x["_embedded"]["venues"]):
                    VenueName.append(ven["name"])
                    VenueAddy.append(ven["address"]["line1"])
        except KeyError:
            print("\nCity Name or State Code Not found!")
            return -1


# creates and prints out a database
def create_database(info, db_name, table_name):
    data = pd.DataFrame.from_dict(info)
    engine = db.create_engine('sqlite:///' + db_name + '.db')
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)
    query_result = engine.execute("SELECT * FROM "+table_name+";").fetchall()
    print(pd.DataFrame(query_result), "\n")


while (True):
    # get input from user and update the city and stateCode parameters
    parameters['city'] = get_city()
    parameters['stateCode'] = get_state()

    # get all events within city and convert to json
    response = requests.get(url, parameters)

    # exit program if request is not successful
    if (response.status_code != 200):
        sys.exit("\nInvalid Request!")

    response = response.json()

    # extracting events details
    checker = extractor(response)
    if (checker == -1):
        print("\nRe-Input City and State")

    else:
        # arranging Event Details into dictionary
        EventDetails = get_dict(eventId, eventName,
                                eventDate, VenueName, VenueAddy)

        # create and return database with details
        create_database(EventDetails, "EVENTS", "Details")

        choice = input("Do you want to check another City(y/n): ").upper()
        if (choice == 'Y'):
            continue
        elif (choice == 'N'):
            exit(0)
        else:
            exit("Input Not Recognise! Bye!")

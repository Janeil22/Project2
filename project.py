import requests

url = "https://app.ticketmaster.com/discovery/v2/events"

API_KEY = "zWmwA15ShfzkNwMGKQ7Ih2RDbAWaoIvV"

parameters = {'apikey':API_KEY, 'countryCode':'US', 'classificationName':'music', 'startDateTime':'2022-07-01T14:00:00Z', 'endDateTime': '2022-08-01T14:00:00Z', 'sort':'date,asc', 'city':'', 'stateCode':''}

parameters['city'] = "Las Vegas" #input("Enter City: ")
parameters['stateCode'] = "NV" #input("Enter State Code: ")

response = requests.get(url, parameters)
response = response.json()



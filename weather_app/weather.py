#Working on it
import requests, json

api_key = "nothing for now"

# base_url variable to store url
base_url = "getting it"

#Data will be requested for this city
city_name = "Ruston"

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)
 
# json method of response object 
# convert json format data into
# python format data
x = response.json()
#Working on it

#Can make it loop and wait to get new data every 30 min
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

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":
 
    # store the value of "main"
    # key in variable y
    y = x["main"]
 
    # store the value corresponding
    # to the "temp" key of y
    current_temperature = y["temp"]
 
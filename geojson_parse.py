import json

# Opening JSON file
f = open('other.geojson')

# returns JSON object as
# a dictionary
data = json.load(f)


# Iterating through the json
# list
for i in data['emp_details']:
    print(i)

# Closing file
f.close()
import requests


# Test that the server is online.
print("----Testing server connection----")
try:
    response = requests.get('http://46.101.199.68:3000/').text
    print(response)
    print("SUCCESS: Server is online and be contacted.")
except requests.exceptions.ConnectionError as e:
    print('ERROR: Connection can not be made with the server. Aborting.')

print("----Testing board reset----")

# Testing the board reset function
try:
    response = requests.get('http://46.101.199.68:3000/reset').text
    #print(response)
    print("SUCCESS: Server allows the reset of board state")
except requests.exceptions.ConnectionError as e:
    print("ERROR: Server unable to reset board state")

print("----Testing tile position setting----")

# Testing if client can set server tile at position
try:
    response = requests.get('http://46.101.199.68:3000/settile?x=4&y=5&char=x&turn=2&player=1').text
    #print(response)
    print("SUCCESS: Server allows the placement of tile from client")
except requests.exceptions.ConnectionError as e:
    print("ERROR: Server unable to set tile position")

print("----Testing request for board state in json format----")

# Testing if client can get board state in json format
try:
    response = requests.get('http://46.101.199.68:3000/getdata').text
    print("\n".join(response.split(']')))
    print("SUCCESS: Server successfully returns board state in json format")
except requests.exceptions.ConnectionError as e:
    print("ERROR: Server unable to return board state in json format")

print("----Testing request for board state in text format----")

# Testing if client can get board state in text format
try:
    response = requests.get('http://46.101.199.68:3000/display').text
    print("\n".join(response.split('<br>')))
    print("SUCCESS: Server successfully returns board state in text format")
except requests.exceptions.ConnectionError as e:
    print("ERROR: Server unable to return board state in text format")

print("----Testing request for last updated turn----")

# Testing if client can get last updated turn
try:
    response = requests.get('http://46.101.199.68:3000/getturn').text
    print(response)
    print("SUCCESS: Server successfully returns last updated turn")
except requests.exceptions.ConnectionError as e:
    print("ERROR: Server unable to return last updated turn")

print("----Testing setting of player rack contents")

# Testing if client can set rack contents for a player
try:
    response = requests.get('http://46.101.199.68:3000/setrack?player=1&rack=[4,2,4,5]').text
    print(response)
    print("SUCCESS: Server accepts rack content change")
except requests.exceptions.ConnectionError as e:
    print("ERROR: Server unable to change player rack contents")

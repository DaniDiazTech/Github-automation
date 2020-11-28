#!/usr/bin/python3

from os.path import expanduser
import sys
import requests
import json

try:
    user = str(sys.argv[1])
except IndexError:
    user = ""
    print("User or repo no specified")

try:
    repository = str(sys.argv[2])
except IndexError:
    repository = ""
    print("User or repo no specified")


# Defines the home directory
home = expanduser("~")


def authentication(path_to_API):
    try:
        with open(path_to_API, 'r') as file:
            # Make sure that your token api is the top of the file

            token = file.readlines()
            real_token = token[0].rstrip("\n")

        return real_token

    except FileNotFoundError:
        print("The File was not found, set a valid path!")


user_token = authentication(f"{home}/Auth/githubapi.txt")
payload = {'name': repository}


# The most important line 
login = requests.post('https://api.github.com/' + 'user/repos',
                      auth=(user, user_token), data=json.dumps(payload))
print("Response from the server : " + str(login.status_code))
print(" ")
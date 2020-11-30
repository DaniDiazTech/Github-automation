#!/usr/bin/python3

import os
import sys
import requests
import json
import time


class OsOperations:
    def __init__(self, name, user, repository_name):
        self.name = name
        self.user = user
        self.repo_name = repository_name

    def make_directory(self):
        """

        :return: Create the project directories
        """
        os.mkdir(self.repo_name)
        os.chdir(self.repo_name)

    def make_git_operations(self):
        """
        :return: Make the Git operations, I prefer to use ssh instead  of Http
        """
        remote = f"git remote add origin git@github.com:{self.user}/{self.repo_name}.git"
        # remote = f"git remote add origin https://github.com/{self.user}/{self.repo_name}.git"

        os.system("git init .")
        os.system("git add .")
        os.system("git commit -m 'Initial commit'")
        os.system("git branch -M main")
        os.system(remote)
        os.system("git push -u origin main")

    def create_files(self):
        mit_license = """        
        MIT License

        Copyright (c) 2020 [year] [full_name] 

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        """
        mit_license.replace("[year]", get_year())
        mit_license.replace("[full_name]", self.name)

        with open("README.md", "w+") as readme:
            readme.write(f"# {self.repo_name}")

        with open("LICENSE", "w+") as my_license:
            my_license.write(mit_license)


# Function that returns the token
def authentication(path_to_api):
    try:
        with open(path_to_api, 'r') as file:
            # Make sure that your token api is the top of the file

            token = file.readlines()
            real_token = token[0].rstrip("\n")

        return real_token

    except FileNotFoundError:
        print("The File was not found, set a valid path!")
        sys.exit()


def get_year():
    """

    :return: Function that return the current year
    """
    year = time.localtime()

    return str(year.tm_year)


print("------- GITHUB AUTOMATION -------")

print("")

print("Your name is required to write the License File")

name = input("Your name >>> ")

user = input("Your github username >>> ")
print("")

print("Make sure that the project name is valid!")

repo_name = input("The name of your repository >>> ")
repository = repo_name.replace(" ", "-")

# print("""
# [1] GNU license
# [2] MIT license
# [3] Apache license
# """)

# license_type = input("License type >>> [1, 2, 3]")
print("")

# Defines the home directory

home = os.path.expanduser("~")

user_token = authentication(f"{home}/Auth/githubapi.txt")

payload = {'name': repository}


# The most important line 
login = requests.post('https://api.github.com/' + 'user/repos',
                      auth=(user, user_token), data=json.dumps(payload))

print("Response from the server : " + str(login.status_code))
print(" ")


# Check if the repo has been created
if str(login.status_code).startswith("2"):
    print("------ Repository Created -------")
    print("")
    print("")
else:
    print("------ Error creating the Repository -------")
    sys.exit()

project = OsOperations(name, user, repository)

pd = os.getcwd()

print(f"Starting repository in  >>> {pd}")

project.make_directory()
project.create_files()
project.make_git_operations()

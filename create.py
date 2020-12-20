#!/usr/bin/python3
"""
Script that automate the boring process of creating a repo on github.
Created by Daniel Diaz.
"""

import os
import shutil
import sys
import json
import time
import requests


class OsOperations:
    """
    Class that makes all Os level operations
    """

    def __init__(self, user, repository_name):
        self.user = user
        self.repo_name = repository_name

    @staticmethod
    def list_dir():
        """ Function that returns the files in the current directory """
        current_dir = os.listdir(os.getcwd())
        print("Created files :", end=" ")
        for i in current_dir:
            print(i, end=", ")
        print("")

    def make_directory(self):
        """

        :return: Create the project directories
        """
        os.mkdir(self.repo_name)
        os.chdir(self.repo_name)

    def make_git_operations(self):
        """
        :return: Make the Git operations, The default remote type is ssh but it can be changed
        if the user type http in command line
        """
        remote_type = GetArguments.get_remote_type()

        # Set the type of remote
        if remote_type == "ssh":
            remote = f"git remote add origin git@github.com:{self.user}/{self.repo_name}.git"
        else:
            remote = f"git remote add origin https://github.com/{self.user}/{self.repo_name}.git"

        # Initialize repository
        os.system("git init .")
        # Add the files previously created
        os.system("git add .")
        # Commit the changes and set a branch "main"
        os.system("git commit -m 'Initial commit'")
        os.system("git branch -M main")
        # Add a  remote  origin with the repo and username
        os.system(remote)
        # Push the changes to github
        os.system("git push -u origin main")

    def get_license_from_templates(self):
        """TODO: Docstring for get_license.

        :returns: License as a str
        """
        # Calls license type, that prompts the user to input License and name
        license_template, name = get_license_type()
        final_license = ""
        # If name resulting of calling license type function is none, it is replaced for the
        # username
        if name is None:
            name = self.user
        # The path where Licenses should be allocated
        license_path = "/.local/share/Github_automation/Templates/LICENSES/"

        # Manage the exception of missing files
        # It asks to install the program if the License files are not founded
        try:
            if license_template == "mit":
                with open(f"{home}{license_path}MIT-license", "r") as license_file:
                    # Reads and replace the name and year brackets founded in
                    # Licenses directory

                    final_license = license_file.read()
                    final_license = final_license.replace(
                        "[year]", get_year()).replace(
                        "[fullname]", name)
            elif license_template == "apache":
                with open(f"{home}{license_path}APACHE-license", "r") as license_file:
                    final_license = license_file.read()
                    final_license = final_license.replace(
                        "[year]", get_year()).replace(
                        "[fullname]", name)

            elif license_template == "mozilla":
                with open(f"{home}{license_path}MOZILLA-license", "r") as license_file:
                    final_license = license_file.read()

            elif license_template == "gnu":
                with open(f"{home}{license_path}GNU-license", "r") as license_file:
                    final_license = license_file.read()
            else:
                final_license = False
        except FileNotFoundError:
            print("The program is not installed, make sure you run:")
            print("./install.sh")
            sys.exit()

        return final_license

    def create_files(self):
        license = self.get_license_from_templates()
        if not license:
            pass
        else:
            with open("LICENSE", "w+") as my_license:
                my_license.write(license)

        with open("README.md", "w+") as readme:
            readme.write(f"# {self.repo_name}")


        # Requires the program to be installed
        ignore_path = f"{home}/.local/share/Github_automation/Templates/python.gitignore"
        ignore_command = f"cp {ignore_path} ./.gitignore"
        os.system(ignore_command)
        print("")
        self.list_dir()


class GetArguments:

    def __init__(self):
        pass

    @staticmethod
    def get_remote_type():
        remote_type = "ssh"
        try:
            first = sys.argv[1]
            if "http" in first or "HTTP" in first:
                remote_type = "https"
        except IndexError:
            pass

        try:
            second = sys.argv[2]
            if "http" in second or "HTTP" in second:
                remote_type = "https"
        except IndexError:
            pass

        return remote_type

    @staticmethod
    def get_editor():
        editor = shutil.which(os.environ.get('EDITOR'))
        try:
            first = sys.argv[1]
            if "http" not in first and "HTTP" not in first:
                argument_editor = shutil.which(first)
                if argument_editor is not None:
                    editor = argument_editor
                else:
                    print(f"{argument_editor} is not a valid editor")
                    print(f"Default editor: {editor} will be used")
        except IndexError:
            pass

        try:
            second = sys.argv[2]
            if "http" not in second and "HTTP" not in second:
                argument_editor = shutil.which(second)
                if argument_editor is not None:
                    editor = argument_editor
                else:
                    print(f"{argument_editor} is not a valid editor")
                    print(f"Default editor: {editor} will be used")
        except IndexError:
            pass

        return editor


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

# If you prefer, to put your token in the code, uncomment the function below
# and comment the  function above
# replace  "Your token here", For your token

# def authentication(path_to_api):
#     return "Your Token here"


# Function that returns the current year
def get_year():
    """

    :return: Function that return the current year
    """
    year = time.localtime()

    return str(year.tm_year)

# Function that create the remote repository

# If the private option  is true, the repo is created as private


def create_repo(username, token, repository_name, private=False):
    """
    Create the repository
    :return: Create the repository
    """
    # Check if the repo for create is private
    if private:
        payload = {'name': repository_name, "private": private}
    else:
        payload = {'name': repository_name}
    
    # Post to the api the json "payload" and the authentication
    # credentials
    
    login = requests.post('https://api.github.com/' + 'user/repos',
                          auth=(username, token), data=json.dumps(payload))
    
    print("Response from the server : " + str(login.status_code))
    print(" ")
   
    # Check if the repo has been created
    if str(login.status_code).startswith("2"):
        print("------ Repository Created -------")
        print("")
    else:
        print("------ Error creating the Repository -------")
        sys.exit()


def launch_editor(editor):
    return os.system(f"{editor} .")


def get_license_type():
    """
    return: The license type and the name of the user if the license need it.
    """
    print("""
    [0] GNU license
    [1] MIT license
    [2] Apache license
    [3] Mozilla license
    [4] No license
    """)

    list_licenses = ["gnu", "mit", "apache", "mozilla", "no"]
    license_type = input("License type >>> [0, 1, 2, 3, 4]")
    name = None
    if license_type == "1":
        name = input("Your name for the MIT license >>> ")

    elif license_type == "2":
        name = input("Your name for the Apache license >>> ")
    # Catch an exception if the input license isn't a number
    try:
        index = int(license_type)
    except ValueError:
        print("License must be a number")
        get_license_type()

    # Catch an exception if the input is out of index
    if name == "" or name == " ":
        name = None

    try:
        return list_licenses[index], name
    except IndexError:
        print("Incorrect number of license")
        get_license_type()


def program_input():
    """TODO: Docstring for program_input.

    :returns: The different arguments needed to perform the program

    """
    print("---------------------------------")
    print("------- GITHUB AUTOMATION -------")
    print("---------------------------------")
    print("")

    username = input("Your github username >>> ")

    print("")
    print("Make sure that the project name is valid!")
    print("")
    repository = input(
        "The name of your repository >>> ").replace(" ", "-")

    print("")
    private = input("The repo is private ? [(y)es, (n)o] >>> ")
    if private == "y" or private == "yes":
        print("")
        print("Private repository created  >>> ")
        print("")
        private_repo = True
    else:
        private_repo = False

    return username, repository, private_repo


def main(user, repository, editor, token, private):
    """

    :param name: Name of the user
    :param user: Github username of the user
    :param repository: Name of the repository that wants to be created
    :param editor: Prefered editor
    :param token: The github auth token
    :return: The repo creation, creation of files and opening of selected editor
    """
    project = OsOperations(user, repository)
    create_repo(user, token, repository, private)
    project.make_directory()
    project.create_files()
    project.make_git_operations()
    launch_editor(editor)


# Variables
home = os.path.expanduser("~")

if __name__ == "__main__":
    user_editor = GetArguments.get_editor()
    user_username, user_repository, user_private = program_input()

    user_token = authentication(f"{home}/Auth/githubapi.txt")

    pd = os.getcwd() + "/" + user_repository

    if shutil.which("git") is not None:
        print(f"Starting repository in  >>> {pd}")
        # Calls the main function if git is installed
        main(
            user_username,
            user_repository,
            user_editor,
            user_token,
            user_private)
    else:
        print(
            "You don't have git installed in your system, install it to create the project")
        sys.exit()

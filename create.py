#!/usr/bin/python3

import os
import shutil
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
        :return: Make the Git operations, The default remote type is ssh but it can be changed
        if the user type http in command line
        """
        remote_type = GetArguments.get_remote_type()

        # Set the type of remote
        if remote_type == "ssh":
            remote = f"git remote add origin git@github.com:{self.user}/{self.repo_name}.git"
        else:
            remote = f"git remote add origin https://github.com/{self.user}/{self.repo_name}.git"

        os.system("git init .")
        os.system("git add .")
        os.system("git commit -m 'Initial commit'")
        os.system("git branch -M main")
        os.system(remote)
        os.system("git push -u origin main")

    def create_files(self):
        mit_license = """
                   MIT License

            Copyright (c) [year] [fullname]

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
            SOFTWARE.
        """
        mit_license = mit_license.replace("[year]", get_year())
        mit_license = mit_license.replace("[fullname]", self.name)

        with open("README.md", "w+") as readme:
            readme.write(f"# {self.repo_name}")

        with open("LICENSE", "w+") as my_license:
            my_license.write(mit_license)

        # Requires the program to be installed
        ignore_file = f"cp {home}/.local/share/Github_automation/Templates/python.gitignore ./.gitignore"
        os.system(ignore_file)


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


def get_year():
    """

    :return: Function that return the current year
    """
    year = time.localtime()

    return str(year.tm_year)


def create_repo(username, token, repository_name):
    """
    Create the repository
    :return: Create the repository
    """
    payload = {'name': repository_name}
    login = requests.post('https://api.github.com/' + 'user/repos',
                          auth=(username, token), data=json.dumps(payload))
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


def launch_editor(editor):
    return os.system(f"{editor} .")


def main(name, user, repository, editor, token):
    """

    :param name: Name of the user
    :param user: Github username of the user
    :param repository: Name of the repository that wants to be created
    :param editor: Prefered editor
    :param token: The github auth token
    :return:
    """
    project = OsOperations(name, user, repository)
    create_repo(user, token, repository)
    project.make_directory()
    project.create_files()
    project.make_git_operations()
    launch_editor(editor)


# Variables
home = os.path.expanduser("~")

if __name__ == "__main__":
    user_editor = GetArguments.get_editor()
    print("------- GITHUB AUTOMATION -------")
    print("")
    print("Your name is required to write the License File")

    user_name = input("Your name >>> ")

    user_username = input("Your github username >>> ")

    print("")
    print("Make sure that the project name is valid!")

    user_repository = input(
        "The name of your repository >>> ").replace(" ", "-")

    # print("""
    # [0] GNU license
    # [1] MIT license
    # [2] Apache license
    # """)

    # license_type = input("License type >>> [0, 2, 3]")
    print("")

    # Defines the Github token

    user_token = authentication(f"{home}/Auth/githubapi.txt")

    pd = os.getcwd() + "/" + user_repository

    if shutil.which("git") is not None:
        print(f"Starting repository in  >>> {pd}")

        main(
            user_name,
            user_username,
            user_repository,
            user_editor,
            user_token)
    else:
        print(
            "You don't have git installed in your system, install it to create the project")
        sys.exit()

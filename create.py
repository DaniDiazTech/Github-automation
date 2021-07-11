#!/usr/bin/python3
"""
Script that automate the boring process of creating a GitHub project.
Created by Daniel Diaz.
"""
import os
import argparse
import subprocess
import getpass
import shutil
import sys
import json
import time

import requests

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

API_URL = "https://api.github.com/"
GITHUB_AUTOMATION_PATH = Path(str(Path().home()) + "/.local/share/Github_automation/")


class GitHubUser:
    """GitHubUser class.

    Authenticate a GitHub user

    Attributes:
        class attributes:
            name: User real name - Used for license choice

        instance attributes:
            username: GitHub username.
            token: GitHub token.
            url:
    """

    name = None

    def __init__(self, username: str = None, token: str = None) -> None:
        """Initialize GitHubUser class."""
        self.username = self.get_username(username)
        self.token = self.get_token(token)
        self.url = API_URL + f'users/{self.username}'

        self.valid_username = self.scrape()

    def scrape(self) -> None:
        """Scrape the GitHub user and check if exists"""

        response = requests.get(self.url, auth=(self.username, self.token))

        if response:
            self.name = response.json()['name']
            self.username = response.json()['login']

            return True

        return False

    def get_token(self, token):
        """Get the GitHub token."""
        if not token:
            return getpass.getpass(prompt='GitHub Token (Or password): ')

        return token

    def get_username(self, username):
        """Get the username."""
        if not username:
            return input('Your GitHub username: ')

        return username

    def get_info(self) -> list:
        """"Get user information."""

        return self.valid_username, self.name, self.token

    def __str__(self) -> str:
        return f'Username: {self.username}, Valid: {self.valid_username}, URL: {self.url}'


class License:
    """Class that holds all the info related to the License of a repo

    Returns:
        License Object: License type, name of user in license file.
    """

    licenses = ['gnu', 'mit', 'apache', 'mozilla']
    licenses_path = GITHUB_AUTOMATION_PATH / 'Templates/LICENSES/'

    # Content: stores the content of the license in an str object
    content = ''

    def __init__(self, choose: str, name: str, licenses_folder: Path = None) -> None:
        """License class constructor

        Args:
            choose (str): The user license choise, must be inside the self.licenses list
            name (str): The real name of the GitHub user
            licenses_folder (Path, optional): Custom license folder. Defaults to None.

        Raises:
            OSError: In case the path to the license folder doesn't exist

        """
        self.choose = choose
        self.name = name
        self.license_folder = self.get_license_folder(licenses_folder)

    def check_choose_is_in_licenses(self) -> bool:
        return self.choose in self.licenses

    def check_path_exists(self, path: Path) -> Path:
        if path.exists():
            return path
        else:
            print('File could not be found')
            print('May GitHub automation is not installed, make sure you ran:')
            print('./install.sh')
            raise OSError()

    # Function that returns the current year

    def get_year(self):
        """

        :return: Function that return the current year
        """
        year = time.localtime()

        return str(year.tm_year)

    def get_license_folder(self, path: Path) -> Path:
        """Gets the path of the license folder and assert it exists"""
        if path and path.exists():
            return path

        path_ = self.licenses_path

        path_ = self.check_path_exists(path_)

        return path_

    def get_licenses_file_names(self) -> dict:

        d = {}

        for license in self.licenses:
            d[license] = self.license_folder / (license.upper() + '-license')

        return d

    def content(self):
        """Returns the content of the license

        Raises:
            OSError: If the choice is not valid
        """

        if not self.check_choose_is_in_licenses():
            print('Choose a valid license name')
            raise OSError

        path = self.get_licenses_file_names().get(self.choose)

        path = self.check_path_exists(path)

        with open(path) as license:

            license = license.read()
            license = license.replace(
                "[year]", self.get_year()).replace(
                "[fullname]", self.name)

        self.content = license

        return self.content


class Repo:
    """
    Class of a github repository.
    Creates and manages a repository on github.
    """
    repo_url = None

    def __init__(self, name: str, user: GitHubUser, description: str = None, license_choice: str = None, private: bool = False, ssh: bool = True) -> None:
        """
        Initialize a repository.
        :param name: Name of the repository.
        :param safe_name: Safe name of the repository. Can be used to create folders.
        :param description: Description of the repository.
        :param path: Path of the repository.
        :param license: License object to write from
        """
        self.name = name
        self.safe_name = self.name.replace(" ", "-")
        self.description = description
        self.user = user
        self.license_choice = license_choice

        self.private = private
        self.ssh = ssh

    def set_repo_url(self):

        end_of_url = f'{self.user.username}/{self.safe_name}.git'

        if not self.ssh:
            self.repo_url = 'https://github.com/' + end_of_url
        else:
            self.repo_url = f'git@github.com:{end_of_url}'

        return self.repo_url

    def create_repo_folder(self):
        """Create the repository folder"""

        # Checks if folder exists manually
        if Path(self.safe_name).exists():
            print(f'Folder {self.safe_name} already exists')
            print('Make sure to delete it before creating a new one')
            raise FileExistsError

        os.mkdir(self.safe_name)

    def enter_repo_folder(self):
        """Enter the repository folder"""
        os.chdir(self.safe_name)

    def create_license(self):
        """Create the license file"""
        if not self.license_choice:
            # Function stops here
            return None

        lc = License(self.license_choice, self.user.name)
        lc = lc.content()

        # Must be on the current directory
        with open("LICENSE", "w+") as file_:
            file_.write(lc)

    def create_readme(self):
        """Create the readme file"""

        readme = f'# {self.name}'

        if self.description:
            readme += f'\n\n{self.description}'

        with open("README.md", "w+") as file_:
            file_.write(readme)

    def create_ignore_file(self):
        """Create the .gitignore file"""

        ignore_path = GITHUB_AUTOMATION_PATH / "Templates/python.gitignore"

        # Copies the file from the template to the current directory
        ignore_command = f"cp {ignore_path} ./.gitignore"

        # Runs the command
        subprocess.run(ignore_command, shell=True)

    def create_files(self):
        """Create the files of the repository, before creating the remote"""

        # Creates repository folder
        self.create_repo_folder()

        # Enter the folder
        self.enter_repo_folder()

        # Create license file
        self.create_license()

        # Create README file
        self.create_readme()

        # Create .gitignore file
        self.create_ignore_file()

    def check_software_installed(self, program: str) -> bool:
        """Check if user has a program installed"""

        if not shutil.which(program):
            print(f'{program} is not installed')
            print(
                f'Make sure to install {program} before running the script again')
            raise OSError

    def check_user_has_git_installed(self):
        """Check if the user has git installed"""
        self.check_software_installed("git")

    def create_remote_repo(self):
        """Create the remote repository"""

        payload = {}

        payload['name'] = self.name

        if self.description:
            payload['description'] = self.description

        if self.private:
            payload['private'] = self.private

        # Post to the api the json "payload" and the authentication
        # credentials

        response = requests.post(
            API_URL + 'user/repos', auth=(self.user.username, self.user.token), data=json.dumps(payload))

        print(f'Response from the server : {str(response.status_code)} \n')

        # Check if the repo has been created
        if response:
            print('------ Repository Created -------\n')
        else:
            print("------ Error creating the Repository -------\n")

            raise OSError

    def create_local_repo(self):
        """Create the local git repository"""

        # Check user has git installed

        # Initialize repository
        subprocess.run('git init', shell=True)

        # Add all files
        subprocess.run('git add .', shell=True)

        # Add a remote origin with the repo and username

        # Commit the changes and set a branch "main"
        subprocess.run("git commit -m 'Initial commit'", shell=True)
        subprocess.run('git branch -M main', shell=True)

        origin_url = self.set_repo_url()

        # Add the remote origin
        subprocess.run(f'git remote add origin {origin_url}', shell=True)

        subprocess.run('git push -u origin main', shell=True)

    def create_repo(self):
        """Create the whole repository"""

        self.check_user_has_git_installed()

        self.create_remote_repo()

        self.create_local_repo()

    def create(self):
        """Runs all the methods"""

        self.create_files()

        self.create_remote_repo()

        self.create_local_repo()


class Main:
    """Class that runs the script

    This class interacts with the user and gets input from him/her

    Use argsparse module to:
        1. Decide if repo use http or ssh
        2. launch an editor after creating the repo
    """

    username = None
    user_token = None
    license = None
    repo_name = None
    repo_description = None

    use_http = False
    private_repo = False
    user_editor = None

    def init_args(self):
        """
        Get all the arguments from the command line using argparse
        and loads them into the class
        """

        parser = argparse.ArgumentParser(
            prog="GitHub automation",
            description="Creates a new github project and its file structure",
            epilog="Happy coding!"
        )

        parser.add_argument(
            "repository_name",
            help="Name of the repository")

        parser.add_argument(
            "-e",
            "--editor",
            help="Editor to open the file",
            default=self.user_editor)

        parser.add_argument(
            "-l",
            "--license",
            choices=License.licenses,
            help="License used in the repo",
        )

        parser.add_argument(
            "-ht",
            "--http",
            action="store_true",
            help="The remote repository will be created with HTTP",
        )

        parser.add_argument(
            "-p",
            "--private",
            action="store_true",
            help="Set the repository to private"
        )

        args = parser.parse_args()

        self.repo_name = args.repository_name
        
        if args.license:
            self.license = args.license

        if args.editor:
            self.user_editor = args.editor

        if args.http:
            self.use_http = True

        if args.private:
            self.private_repo = True


    def get_editor(self):
        """
        Gets the editor from the user

        If not editor provider by the user, it'll use 
        editor from the system
        """

        if self.user_editor:
            return self.user_editor

        return os.environ.get('EDITOR', 'vim')

    def launch_editor(self):
        """Launch the editor"""

        subprocess.run(self.get_editor() + ' ./', shell=True)

    def print_program_welcome(self):
        """
        Prints the program welcome 
        """
        print("""
        ---------------------------------
        ------- GITHUB AUTOMATION -------
        ---------------------------------
        """)

    def print_license_choice(self):
        """Prints the license options"""
        print("""
        Please, choose a license,

        gnu: GNU license
        mit: MIT license
        apache: Apache license
        mozilla: Mozilla license
        no: No license
        """)

    def get_username_and_token(self):
        """Gets the username and token from environmentable variables"""

        username = os.environ.get('GITHUB_USERNAME')
        token = os.environ.get('GITHUB_TOKEN')

        return username, token

    def get_description(self):
        return input('Project description: ')

    def get_license_choice(self):
        """Returns the user license choice"""
        if not self.license:
            self.print_license_choice()
            choice = input('Choose a license: ')
            choice = choice.lower()

            if not choice in License.licenses:
                return None
            
            self.license = choice

        return self.license


    def run(self):
        """Runs the script"""
        self.init_args()
        self.print_program_welcome()

        self.username, self.user_token = self.get_username_and_token()

        user = GitHubUser(self.username, self.user_token)

        ssh = not self.use_http

        repo = Repo(
            self.repo_name,
            user,
            description=self.get_description(),
            license_choice=self.get_license_choice(),
            private = self.private_repo,
            ssh=ssh
        )

        repo.create()

        self.launch_editor()

if __name__ == '__main__':
    main = Main()
    main.run()
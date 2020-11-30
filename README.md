# Github automation

This is a program that help you to automate the boring process of creating a project on github.

## Steps you are avoiding:

You are saving a lot of time by using a github automation tool. You are skipping:

1. Create a repo in the Github Website
2. Create the header of the **README** and pasting the **LICENSE**
3. Doing the boring stuff with git:
    
    * Git init
    * Git add .
    * Git commit -m
    * Git add remote


## Dependencies

* Python3
* Vscodium or Vscode

Consider to install [Vscodium](https://vscodium.com/) instead of Vscode, since Vscodium is the open-source binary of Vscode.

Also you need a **github access token**. You can find it by **Going to your Settings > Developer settings > Personal access tokens > Generate access tokens**.

I selected the repo and Workflow boxes.

## Installation

First you need to clone the repository:

```
git clone https://github.com/Daniel1404/Github-automation.git
```
Then make the installation process:

```
cd Github-automation
```

```
./install.sh
```
Now the program should be copied in .local/share/Github-automation, so you could erase the current directory.

## Usage 

By default you just need to create a folder named **/Auth** in your home directory, and paste your github token in the first line of a new file named **githubapi.txt**.

You can do it with the following commands:

```
cd ~
mkdir Auth
cd Auth/
cat >> githubapi.txt <<EOF
"YOUR TOKEN IN THE FIRST LINE"
EOF
```
Warning: I know that having your token in a plain text file, would be risky. So I will try to do something in this aspect.

Now type create in your terminal.

```
create
```

This will call the **[create.py](https://github.com/Daniel1404/Github-automation/blob/main/create.py)** file.

You will see a prompt where you have to type your name (To include it in the MIT License), your github username and the name of the repo you want to create.

## Screenshot
![Creating a repo](.screenshots/create.png "Creating a repo")

That's all.

## TO-DO's

* Implement License choose, since the default license is always the MIT license
* Find a more secure way to use the token
* Make it usable in Windows.
* Implement a text editor choice in installation process.


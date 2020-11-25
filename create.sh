#!/bin/bash

### GITHUB AUTOMATION BY DANIEL DIAZ ###
#
#  ____   ____
# |  _ \ |  _ \   Copyright (c) 2020 Daniel Diaz
# | | | || | | |
# | |_| || |_| |  http://www.github.com/Daniel1404/Github_automation
# |____/ |____/
#


read -p "Your username >>> " user
read -p "Name of the new project >>> " repo

python3 create.py $user $repo 

echo "--------Repository Created ---------"

echo " "
echo " "
echo " "
echo "-------Setting up git locally------"
echo "  "

mkdir $repo

cd $repo 

git init .

echo "  "

touch README.md
touch .gitignore

# I use SSH

echo " ----------- Setting remote ------------ "
echo "  "
echo "  "

# You could use http by uncomment next line
# git remote add origin https://github.com/$user/$repo.git

# Storing repository's path

Project=$(pwd)

echo "Project created at >>>  $Project"

echo " "


git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:$user/$repo.git
git push -u origin main

echo " "
echo "Launching Vs code"
code . 

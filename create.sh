#!/bin/bash

# $1 -> Contains project name.
# $2 -> Contains environment to put in .gitignore  


echo "------- CREATED BY DANIEL DIAZ 2020  --------"

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

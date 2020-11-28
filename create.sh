#!/bin/bash

### GITHUB AUTOMATION BY DANIEL DIAZ ###
#
#  ____   ____
# |  _ \ |  _ \   Copyright (c) 2020 Daniel Diaz
# | | | || | | |
# | |_| || |_| |  http://www.github.com/Daniel1404/Github_automation
# |____/ |____/
#


# LOCATION=$(pwd)

# echo $LOCATION

echo "------- GITHUB AUTOMATION -------"
echo " "
echo " "

echo "Your name is required to write the License File"
read -p "Your name >>> " name
echo " "
echo "Make sure the name of your project is valid !"
echo " "
read -p "Your username on github >>> " user
read -p "Name of the new project >>> " repo

# Call create_py binary, once ./install has been used
# Allows to create the repo on Github

create_py $user $repo 

echo "------ Repository Created ------"

echo " "
echo " "
echo " "

echo "------ Setting up git locally ------"
echo "  "

mkdir $repo

cd $repo 

git init .

echo "  "

cat >> README.md <<EOF
# $repo
EOF

touch .gitignore

cat >> LICENSE <<EOF
MIT License

Copyright (c) 2020 $name 

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

EOF

# I use SSH

echo " ------ Setting remote ------"
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
echo "Launching Vs code ..."
code . 

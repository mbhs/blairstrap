#!/bin/bash

# Read config file
config="config.ini"
url=$(awk '/url/ {print $2}' $config)
branch=$(awk '/branch/ {print $2}' $config)
commit=$(awk '/commit/ {print $2}' $config)
name=$(awk '/name/ {print $2}' $config)
location=$(awk '/location/ {print $2}' $config)
destination=$(awk '/destination/ {print $2}' $config)

out="$destination/$name/"

# Check whether a directory is a git repository
check_git_repository() {

  # Check directory
  if [ ! -d $1 ]; then return 1; fi
  
  # Check rev-parse and remote url
  local result=1
  pushd $1 > /dev/null
  if [ -d .git ] || git rev-parse --git-dir > /dev/null; then
    if [ $(git config --get remote.origin.url) = $2 ]; then
      result=0;
    else result=1; fi
  else result=2; fi

  popd > /dev/null
  return $result
  
}

echo "Checking $location is $url"
if check_git_repository $location $url; then
  echo "Correct repository and URL."
else
  echo "Invalid repository or URL."
  if [ -d $location ]; then
    read -p "Overwrite files at $location? [Y/n]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      rm -r $location
    else exit 1; fi
  fi
  git clone $url $location
fi

pushd $location > /dev/null
git reset --hard
git pull
git checkout $commit
popd > /dev/null
cp scss/* $location/scss/

pushd $location > /dev/null
echo $(pwd)
npm install grunt grunt-cli
npm install
grunt dist

if [ -d $out ]; then rm -rf $out; fi
if [ ! -d $destination ]; then mkdir -p $destination; fi

mv dist/ $out

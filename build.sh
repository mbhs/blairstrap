#!/bin/bash

# Read config file
config="config.ini"
url=$(awk '/url/ {print $2}' $config)
branch=$(awk '/branch/ {print $2}' $config)
commit=$(awk '/commit/ {print $2}' $config)
location=$(awk '/location/ {print $2}' $config)


# Check whether a directory is a git repository
is_git_repository() {
  if [ ! -d $1 ]; then return 1; fi
  local result=1
  pushd $1 > /dev/null 2>&1
  if [ -d .git ] || git rev-parse --git-dir > /dev/null 2>&1; then result=0; fi
  popd > /dev/null 2>&1
  return $result;
}


if is_git_repository "/tmp/bootstrap"; then
  echo "Repository"
else
  echo "Not repository"
fi


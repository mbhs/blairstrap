"""Script for building bootstrap with custom configurations.

The runtime consists of cloning bootstrap, copying over the provided
SCSS files into the corresponding directory, and building to the 
specified distribution path.
"""

import sh
import shutil
import os
import re
import sys


OFFLINE = True  # mfw on plane
OFFLINE_COPY = "/Users/Noah/Static/bootstrap"


def catch_keyboard_interrupt(function):
    """Fail gracefully if the shell is interrupted."""

    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except KeyboardInterrupt:
            print("User interrupted!")
            sys.exit(0)
    return wrapper


@catch_keyboard_interrupt
def clone(url: str, to: str, branch: str=None, commit: str=None):
    """Clone a git repository to a location."""

    cwd = os.getcwd()

    print("Sanitizing inputs...")
    assert url
    assert to

    print("Checking clone location...")
    delete = False
    clone = True
    if os.path.isdir(to):
        os.chdir(to)
        try:
            existing = sh.git.config("--get", "remote.origin.url").strip()
            print("Existing git repository found.")
        except sh.ErrorReturnCode_1:
            print("No git repository at found.")
            delete = True
        else:
            if existing == url:
                print("Found existing bootstrap repository.")
                print("Resetting and updating...")
                sh.git.reset("--hard")
                if not OFFLINE:
                    sh.git.pull()
                clone = False
            else:
                print("Found other repository.")
                delete = True
        os.chdir(cwd)
    elif os.path.exists(to):
        print("Found file at location.")
        delete = True

    if delete:
        if input("Delete existing files at {}? [Y/n] ".format(to)).lower() == "y":
            shutil.rmtree(to)
            print("Deleted.")
        else:
            print("Exiting...")
            sys.exit(0)

    if clone:
        print("Cloning new repository...")
        if OFFLINE:
            print("Copying offline version...")
            sh.cp("-r", OFFLINE_COPY, to)
        else:
            sh.git.clone(url, to)
    os.chdir(to)
    if branch:
        sh.git.checkout(branch)
    if commit:
        sh.git.checkout(commit)
    os.chdir(cwd)


@catch_keyboard_interrupt
def build(to: str):
    """Build bootstrap at the specified location."""

    cwd = os.getcwd()
    os.chdir(to)
    print("Installing NPM dependencies...")
    os.system("npm install")
    os.system("npm install -g grunt-cli")
    print("Rebuilding css...")
    os.system("npm run css")
    os.chdir(cwd)


if __name__ == "__main__":
    """Run as a shell script."""

    import argparse
    import sys
    import glob

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://github.com/twbs/bootstrap.git")
    parser.add_argument("--branch", default=None)
    parser.add_argument("--commit", default=None)
    parser.add_argument("-b", "--build", default="/tmp/bootstrap/")
    parser.add_argument("-n", "--nocache", action="store_true", default=False)
    parser.add_argument("-o", "--out", default="./bootstrap/")

    args = parser.parse_args(sys.argv[1:])

    clone(args.url, args.build, args.branch, args.commit)
    sh.cp(*glob.glob("scss/*"), os.path.join(args.build, "scss"))
    build(args.build)
    sh.mv(os.path.join(args.build, "dist"), args.out)

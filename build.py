"""Script for building bootstrap with custom configurations.

The runtime consists of cloning bootstrap, copying over the provided
SCSS files into the corresponding directory, and building to the 
specified distribution path.
"""

import sh
import shutil
import os
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
    return wrapper


@catch_keyboard_interrupt
def clone(url: str, to: str, branch: str=None, commit: str=None):
    """Clone a git repository to a location."""

    print("Sanitizing inputs...")
    assert url
    assert to

    print("Checking clone location...")
    delete = False
    if os.path.isdir(to):
        try:
            existing = sh.git.config("--get", "remote.origin.url")
            print("Existing git repository found.")
        except sh.ErrorReturnCode_1:
            print("No git repository at found.")
            delete = True
        else:
            if existing == url:
                print("Found existing bootstrap repository.")
            else:
                print("Found other repository.")
                delete = True
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

    print("Cloning new repository...")
    if OFFLINE:
        print("Copying offline version...")
        sh.cp("-r", OFFLINE_COPY, to)
    else:
        sh.git.clone(url, to)

    sh.pushd(to)
    if branch:
        sh.git.checkout(branch)
    if commit:
        sh.git.checkout(commit)
    #sh.popd()


if __name__ == "__main__":
    """Run as a shell script."""

    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://github.com/twbs/bootstrap.git")
    parser.add_argument("--branch", default=None)
    parser.add_argument("--commit", default=None)
    parser.add_argument("-b", "--build", default="/tmp/bootstrap")
    parser.add_argument("-n", "--nocache", action="store_true", default=False)
    parser.add_argument("-o", "--out", default="./bootstrap")

    args = parser.parse_args(sys.argv[1:])

    clone(args.url, args.build, args.branch, args.commit)


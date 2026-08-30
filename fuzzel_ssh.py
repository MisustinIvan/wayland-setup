#!/usr/bin/python3
from subprocess import Popen, PIPE
import sys
import json
import os


def notify(subject, body):
    print(body)
    Popen(['notify-send', subject, body])

def get_selection(input_list, prompt="", max_lines=8) -> str:
    length = str(min(len(input_list), max_lines))
    with Popen(
        ["fuzzel", "--dmenu", "-l", length, "-p", prompt],
        stdin=PIPE, stdout=PIPE, stderr=PIPE
    ) as fuzzel:
        selection = fuzzel.communicate(
            input=bytes("\n".join(input_list), 'utf-8'))[0]
        if fuzzel.returncode != 0:
            sys.exit(1)
        return selection.decode().strip()


def main():
    config = {'work': 'mr-crabs', 'factorio': 'factorio'}
    selection = get_selection(list(config), prompt="Select a machine: ")
    Popen(['alacritty', '-e', 'ssh', config[selection], '-t', 'tmux', 'a'])

if __name__ == "__main__":
    main()

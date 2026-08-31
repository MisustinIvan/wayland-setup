#!/usr/bin/env python3
from subprocess import Popen, PIPE
import sys


def get_input(prompt: str = "") -> str:
    cmd = ["fuzzel", "--dmenu", "--prompt-only", prompt]
    with Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE) as fuzzel:
        stdout, _ = fuzzel.communicate(input=b"")
        if fuzzel.returncode != 0:
            sys.exit(0)
        return stdout.decode().strip()


def main():
    code = get_input(prompt="Eval: ")
    if not code:
        return

    try:
        res = eval(code)
    except Exception as e:
        res = f"Error: {e}"

    get_input(prompt=f"{res} ")


if __name__ == "__main__":
    main()

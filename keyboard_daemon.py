#!/usr/bin/env python3
import json
import subprocess
import sys
import time
import hid

VENDOR_ID = 0x3434
USAGE_PAGE = 0xFF60
USAGE = 0x61

def get_device():
    for dev in hid.enumerate(VENDOR_ID):
        if dev.get('usage_page') == USAGE_PAGE and dev.get('usage') == USAGE:
            try:
                path = dev['path']
                if isinstance(path, str):
                    path = path.encode('utf-8')
                return hid.Device(path=path)
            except Exception as e:
                print(f"[-] Failed to open device: {e}", file=sys.stderr)
                return None
    return None

def send_layout_state(dev, is_czech):
    val = 1 if is_czech else 0
    pkt = bytes([0x00, 0x07, 0x01, 0x00, val] + [0x00] * 28)
    try:
        dev.write(pkt)
        return True
    except Exception as e:
        print(f"[-] HID write failed: {e}", file=sys.stderr)
        return False

def listen_niri_events():
    dev = None

    while True:
        while not dev:
            print("[*] Connecting to Keychron V1...")
            dev = get_device()
            if not dev:
                time.sleep(2)
        print("[+] Connected to keyboard.")

        try:
            proc = subprocess.Popen(
                ["niri", "msg", "--json", "event-stream"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
        except FileNotFoundError:
            print("[-] 'niri' command not found.", file=sys.stderr)
            time.sleep(5)
            continue

        # Use iter(proc.stdout.readline, '') to prevent pipeline stalls
        for line in iter(proc.stdout.readline, ''):
            line_str = line.strip()
            if not line_str:
                continue

            try:
                event = json.loads(line_str)
            except json.JSONDecodeError:
                continue

            if "KeyboardLayoutSwitched" in event:
                layout_data = event["KeyboardLayoutSwitched"]
                layout_idx = layout_data.get("idx")

                # Check for idx == 1 or check by name if present
                is_czech = (layout_idx == 1)
                print(f"[+] Event captured: idx={layout_idx} -> is_czech={is_czech}")

                if not send_layout_state(dev, is_czech):
                    try:
                        dev.close()
                    except Exception:
                        pass
                    dev = None
                    break

        if proc:
            proc.terminate()
        time.sleep(1)

if __name__ == "__main__":
    listen_niri_events()

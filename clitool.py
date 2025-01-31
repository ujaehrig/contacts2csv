#!/usr/bin/env -S uv run --script

import sys

from library import csv2ical

def main():
    # Read from stdin or first argument
    input_file = sys.stdin.buffer
    if len(sys.argv) > 1:
        input_file = open(sys.argv[1], 'rb')

    try:
        contacts = csv2ical.process_csv(input_file)
        ical_data = csv2ical.generate_ical(contacts)
        sys.stdout.buffer.write(ical_data)
    finally:
        if input_file != sys.stdin.buffer:
            input_file.close()


if __name__ == '__main__':
    main()

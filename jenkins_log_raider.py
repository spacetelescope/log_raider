import argparse
import os
import sys


PIPELINE_MARKER = "[Pipeline]"
PIPELINE_BLOCK_START = '{'
PIPELINE_BLOCK_START_NOTE = '('
PIPELINE_BLOCK_START_NOTE_END= ')'
PIPELINE_BLOCK_END = '}'
PIPELINE_BLOCK_END_NOTE = "//"

def consume_token(s, token):
    return s[s.find(token) + len(token) + 1:]


def parse_log(filename):
    block_depth = 0
    block_reading = False
    data = open(filename, "r").read()
    for lineno, line in enumerate(data.splitlines()):
        # Consume pipeline marker
        if line.startswith(PIPELINE_MARKER):
            event_type = ""
            event_name = ""
            line = consume_token(line, PIPELINE_MARKER)

            if line.startswith(PIPELINE_BLOCK_END):
                line = consume_token(line, PIPELINE_BLOCK_END)
                block_reading = False
                block_depth -= 1

                print(f"Block depth: {block_depth}")
            elif line.startswith(PIPELINE_BLOCK_END_NOTE):
                continue

            if line.startswith(PIPELINE_BLOCK_START):
                line = consume_token(line, PIPELINE_BLOCK_START)
                if line.startswith(PIPELINE_BLOCK_START_NOTE):
                    event_name = line[1:len(line) - 1]
                block_reading = True
                block_depth += 1
                print(f"Block depth: {block_depth}")
            else:
                event_type = line

            if event_type:
                print(f"[{lineno}] Event Type: {event_type}")
            if event_name:
                print(f"[{lineno}] Event Desc.: {event_name}")

        elif block_reading:
            print(f"[{lineno}] Data: {line}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('logfile')
    args = parser.parse_args()

    if not os.path.exists(args.logfile):
        print(f"{args.logfile}: does not exist")

    parse_log(args.logfile)


if __name__ == "__main__":
    sys.exit(main())


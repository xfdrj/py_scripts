# Requests and errors per hour (CLI)
#
# Command-line tool that groups access log requests by hour and reports,
# for each hour, the total number of requests and the number of responses
# with status >= --min-status.
#
# Input:   path to a directory containing access_*.log files
# Options: --min-status  status code from which a response counts as an error (default: 500)
#          --top         number of rows to show (default: all)
# Output:  table with columns hour, total, errors
# Tools:   Python standard library (argparse, re, pathlib, collections)
#
# Usage:
#
#   python <filename>.py logs
#   python <filename>.py logs --min-status 400 --top 2
#
# Example output (--min-status 500):
#
#   hour              total  errors
#   10/Oct 13:00        6      2
#   10/Oct 14:00       10      2
#   10/Oct 15:00        3      1

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys

# 203.0.113.9 - - [10/Oct/2026:14:10:15 +0000] "POST /login HTTP/1.1" 401 96 "-" "Mozilla/5.0"
# 203.0.113.9 - - [10/Oct/2026:14:10:19 +0000] "POST /login HTTP/1.1" 500 128 "-" "Mozilla/5.0"
reg = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - '
    r'\[(?P<date>\d{2}/\w{3}/\d{4}):(?P<hour>\d{2}):\d{2}:\d{2} \+0000\] '
    r'"(?P<method>\w+) (?P<event>\S+) HTTP/1.1" '
    r'(?P<status>\d{3}) (?P<response>\d+)'
)

def parse_line(line):
    match = reg.match(line)
    if match is None:
        return None
    else: return match.groupdict()
    
def main(arg, min_status, top):
    failures = defaultdict(Counter)
    for path in Path(arg).glob("access_*.log"):
        with open (path, encoding="utf-8", errors="replace") as f:
            for line in f:
                record = parse_line(line)
                if record is None: continue
                dict_key = f'{record["date"][:6]} {record["hour"]}:00'
                failures[dict_key]["total"] +=1
                if int(record["status"]) >=min_status:
                    failures[dict_key]["errors"] +=1
    print(f'{"hour":<18}{"total":>5}{"errors":>8}')
    for hour in sorted(failures)[:top]:
        counts = failures[hour]
        print(f'{hour:<18}{counts["total"]:>5}{counts["errors"]:>8}')

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--min-status", type=int, default=500)
    parser.add_argument("--top", type=int, default=None)
    args=parser.parse_args()
    main(args.path, args.min_status, args.top)
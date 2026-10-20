# Top IPs and top paths from access logs
#
# Reads "combined" format access logs (access_1.log, access_2.log),
# parses each line into ip, timestamp, method, path and status, and prints
# the most frequent client IPs and the most requested paths.
# Lines that do not match the log format are skipped and counted.
#
# Input:   access_*.log files
# Output:  number of parsed and skipped lines, top IPs, top paths
# Tools:   Python standard library (re, collections.Counter)
#
# Example output:
#
#   parsed 19, skipped 1
#   Top IPs:
#     203.0.113.5    6
#     198.51.100.7   5
#     192.0.2.44     4
#     203.0.113.9    4
#   Top paths:
#     /api/nodes     7
#     /index.html    4
#     /login         4
#     /api/jobs      3
#     /favicon.ico   1

import re
import sys
from collections import Counter

reg = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<time>\d+/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) \+\d{4}\] "(?P<method>\w+) (?P<path>\S+)')

def parse_line(line):
    match=reg.match(line)
    if match is None:
        return None
    return match.groupdict()

def main(paths):
    skipped = 0
    parsed = 0
    ip_dict = {}
    path_dict = {}
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, start=1):
                record = parse_line(line)
                if record is None:
                    skipped+=1
                    continue
                else:
                    parsed +=1
                    ip_dict[record["ip"]]=ip_dict.setdefault(record["ip"], 0) + 1
                    path_dict[record["path"]]=path_dict.setdefault(record["path"], 0) + 1  
    top_ips = Counter(ip_dict).most_common() 
    top_paths = Counter(path_dict).most_common() 
    
    print(f"parsed: {parsed}, skipped: {skipped}")
    print(f"Top IPs:")
    for ips, counter in top_ips:
        print(f"{ips}: {counter}")
    print(f"Top PATHs:")
    for paths, counter in top_paths:
        print(f"{paths}: {counter}")
        
if __name__ == "__main__":
    main(sys.argv[1:])
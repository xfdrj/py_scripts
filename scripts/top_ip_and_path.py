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
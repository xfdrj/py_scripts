from collections import Counter, defaultdict
from pathlib import Path
import re
import sys

#203.0.113.9 - - [10/Oct/2026:14:10:19 +0000] "POST /login HTTP/1.1" 500 128 "-" "Mozilla/5.0"
#192.0.2.44 - - [10/Oct/2026:14:15:00 +0000] "GET /api/nodes HTTP/1.1" 200 512 "-" "Mozilla/5.0"

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
    
def main(arg):
    results = defaultdict(Counter) #ip: total_request_amount - 500+_amount_(errors)
    folder = Path(arg)
    for path in folder.glob("access_*.log"):
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                record=parse_line(line)
                if record is None:
                    continue
                results[record["ip"]]["total"]+=1
                if int(record["status"])>=500:
                    results[record["ip"]]["errors"]+=1
        
    def error_share(ip):
        return results[ip]["errors"] / results[ip]["total"]

    for ip in sorted(results, key=error_share, reverse=True):
        c = results[ip]
        print(f'{ip}: {c["errors"]}/{c["total"]}  {round(error_share(ip) * 100)}%')
        
if __name__=="__main__":
    main(sys.argv[1])
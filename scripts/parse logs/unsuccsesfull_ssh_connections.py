# Failed SSH logins by source IP
#
# Parses sshd entries from auth.log (two hosts: gpu-node-01, gpu-node-02)
# and counts failed password attempts per source IP, with a per-host breakdown.
# "invalid user" attempts are counted as failures. Successful logins,
# closed connections and pam_unix "authentication failure" lines are ignored.
#
# Input:   auth.log
# Output:  source IPs sorted by number of failures, with counts per host
# Tools:   Python standard library (re, collections.defaultdict, collections.Counter)
#
# Example output:
#
#   203.0.113.50   4   (gpu-node-01: 3, gpu-node-02: 1)
#   198.51.100.23  3   (gpu-node-02: 3)
#   192.0.2.77     1   (gpu-node-01: 1)

from collections import Counter, defaultdict
import re
import sys


reg = re.compile(r'(?P<date>\w{3} \d{2} \d{2}:\d{2}:\d{2}) (?P<node>gpu-node-\d{2}) (?P<ssh>sshd\[\d+\]): ((?P<status>[A-Za-z]+) \w+ for (?:invalid user )?\S+ from (?P<ip>\d+\.\d+\.\d+\.\d+) port (?P<port>\d+) ssh2|(pam_unix\(sshd:auth\): authentication failure; (?P<details>logname= uid=\d+ euid=\d+ tty=sshrhost=\d+\.\d+\.\d+\.\d+) user=root))')

def parse_line(line):
    match=reg.match(line)
    if match is None:
        return None
    else: return match.groupdict()
    

    
def main(paths):
    failures=defaultdict(Counter)
    for path in paths:
        with open (path, errors="replace", encoding="utf-8") as f:
            for line in f:
                record = parse_line(line)
                if record is None or record["status"] != "Failed":
                    continue
                failures[record["ip"]][record["node"]] += 1
    
    def total_failures_for_ip(ip):
        return sum(failures[ip].values())
    
    for ip in sorted(failures, key=total_failures_for_ip, reverse=True):
        parts = []
        for node, count in sorted(failures[ip].items()):
            parts.append(f"{node}: {count}")
        detail = ", ".join(parts)

        print(f"{ip} {total_failures_for_ip(ip)} ({detail})")
    
if __name__=="__main__":
    main(sys.argv[1:])
    
import ipaddress
import json
import csv
import sys
import os
from ping3 import ping

RESULT_FILE = "result.csv"


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_ranges(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)

    if "ranges" not in data or not isinstance(data["ranges"], list):
        raise ValueError("JSON must contain a list called 'ranges'")

    return data["ranges"]


def ensure_csv_header():
    if not os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["cidr", "ip", "status", "rtt_ms"])


def ping_ranges(json_file, timeout):
    ranges = load_ranges(json_file)
    ensure_csv_header()

    with open(RESULT_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        for cidr in ranges:
            network = ipaddress.ip_network(cidr, strict=False)
            hosts = list(network.hosts())
            total = len(hosts)

            log(f"\n[+] Scanning {cidr} ({total} hosts)")

            for idx, ip in enumerate(hosts, start=1):
                ip_str = str(ip)
                log(f"[{idx}/{total}] Pinging {ip_str}")

                try:
                    rtt = ping(ip_str, timeout=timeout)
                    if rtt is not None:
                        writer.writerow([cidr, ip_str, "alive", round(rtt * 1000, 2)])
                        log(f"    [ALIVE] {ip_str}")
                    else:
                        writer.writerow([cidr, ip_str, "dead", ""])
                except Exception as e:
                    writer.writerow([cidr, ip_str, "error", str(e)])
                    log(f"    [ERROR] {ip_str} ({e})")

    log(f"\n[+] All results saved to {RESULT_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ping_ranges.py ranges.json")
        sys.exit(1)

    json_file = sys.argv[1]
    ping_ranges(json_file, timeout=1)

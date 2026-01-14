# status-ping-with-range

This project helps you check the **ping status of IP addresses in CIDR ranges**.

You define one or more IP ranges in a JSON file, then the script pings all IPs in those ranges and saves the results to a CSV file.

---

## 📌 Features

- Ping IP addresses from CIDR ranges
- Read multiple ranges from a JSON file
- Automatically creates `result.csv`
- Appends results if the file already exists
- No output filename required
- Uses `ping3`

---

## 📄 Example JSON File

Create a file called `ranges.json`:

```json
{
  "ranges": [
    "192.168.20.0/20",
    "125.26.14.0/24"
  ]
}

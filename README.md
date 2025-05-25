# Clarity AI Log Parser

This tool was built as part of the **Clarity AI challenge**. It reads a log file and returns all hosts that connected to a specified target host during a given time window.

---

## 🧩 Challenge Description

### Task 1:  
Build a tool that, given:

- A log file path
- A `start_datetime`
- An `end_datetime`
- A `target_host`

...returns a list of all hostnames that were connected to the target host during that time window.

---

## 📄 Input Format

The log file has one connection per line:

<timestamp> <hostA> <hostB>

Example:

1704068314 host22 host29


- The **timestamp** is in **UNIX epoch format** (seconds since Jan 1st, 1970).
- Hostnames are simple identifiers like `host22`, `host29`.

---

## ⚙️ Assumptions

- **Connections are bidirectional.**  
  `host22 host29` means both hosts were involved in a connection.
  Therefore, the parser checks both columns: source and destination.

- **Malformed lines** are skipped (e.g. missing fields, invalid timestamp).

- **Time ranges are inclusive**:  
  A timestamp exactly equal to the start or end time will be considered.

---

## 🚀 Usage

### CLI Command

```bash
python main.py <logfile> <host> "<start_time>" "<end_time>"
```

### Example

python main.py data/Optional-connections.log host22 "2024-01-01 00:00:00" "2024-12-30 23:59:59"

### Output

Hosts connected to 'host22' between 2024-01-01 00:00:00 and 2024-12-30 23:59:59:
- host29
- host35

## 🧪 Run Tests

Run unit tests using pytest:

make test

## 📦 Dependencies

Install them with:

make install

Freeze to requirements.txt:

make freeze

Currently only pytest is required

## 📁 Project Structure

├── src/
│   └── parser.py         ← Core parsing logic
├── main.py               ← CLI entry point
├── tests/
│   └── test_parser.py    ← Unit test
├── data/                 ← Log file(s)
├── requirements.txt
└── README.md

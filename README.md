# Clarity AI Log Parser

This tool was built as part of the **Clarity AI challenge**. It processes a log file of network connections to extract insights about host communications.

---

## 🧩 Challenge Description

### ✅ Task 1 – Query Hosts in Time Range (Completed) 
Build a tool that, given:
- A log file path
- A `start_datetime`
- An `end_datetime`
- A `target_host`

...returns a list of all hostnames that were connected to the target host during that time window.

🛠️ Implemented in: [`main.py`](main.py)  
📦 Core logic: [`src/parser.py`](src/parser.py)  
✅ Status: **Completed**

---

### ✅ Task 2 – Stream Monitoring in Batch Mode (Completed)

Build a tool that processes network connection logs and reports:

- ✅ Hosts that connected **to** a target host (`--incoming`)
- ✅ Hosts that a target host connected **to** (`--outgoing`)
- ✅ The host with the most total connections
- ✅ Works in **batch mode** over a user-defined time window (`--frequency`)

🛠️ Implemented in: [`stream.py`](stream.py)  
📦 Core logic: [`src/stream_monitor.py`](src/stream_monitor.py)  
✅ Status: **Completed (Batch Mode)**  
❌ Streaming mode not implemented

---

## 🔮 Future Work

### ⏳ Features to Implement

- 🛰️ **Streaming mode**: Support real-time log processing by continuously monitoring a log file (see design below).
- 🧪 Add more robust unit tests for `stream_monitor.py`
- 🧼 Add input validation and structured logging (e.g., with Python `logging` module)
- ✅ Refactor and document code for better modularity and reusability
- 🔔 Log warnings for malformed lines instead of skipping silently

---

### 🛰️ Real-Time Streaming Mode (Design Plan)

To extend Task 2 into a streaming solution, the parser would operate continuously, reading new log lines and emitting reports periodically.

#### ✅ Objectives

- Monitor a log file in real time as new connections are logged.
- Maintain a sliding time window (e.g., last hour) of logs.
- Periodically emit updated connection reports.

#### ⚙️ Design Steps

1. **Open and seek to end of log file**  
   Mimic the behavior of `tail -f` in Linux:
   > Continuously read and output appended lines as the file grows.

2. **Read new lines as they're written**  
   Use a polling loop:
   ```python
   while True:
       line = logfile.readline()
       if not line:
           time.sleep(0.5)
           continue
       process(line)
    ```
3. **Maintain a sliding window**  
   Use a `deque` to keep only log lines from the last `frequency` seconds:
   ```from collections import deque
    sliding_window = deque()
    ```
4. **Emit reports periodically**  
   Every `self.frequency` seconds:

   - Remove outdated log entries from the deque based on their timestamp.
   - Generate and print the following insights:
     - 🔻 Hosts that connected **to** the target host (incoming).
     - 🔺 Hosts the target host connected **to** (outgoing).
     - 🏆 Host with the **most total connections** in the current time window.

#### 📦 Tools & Techniques

- `deque` from `collections`  
  Efficient data structure for maintaining a sliding window (append to right, pop from left).

- `time.time()`  
  Used to compare current timestamp with each log's timestamp to keep the window accurate.

- `time.sleep()`  
  Pauses the loop to reduce CPU usage while polling the file.

- `readline()`  
  Reads only the newly appended lines to the log file (like `tail -f` behavior).


## 📄 Input Format

The log file has one connection per line:

<timestamp> <hostA> <hostB>

Example:

1704068314 host22 host29


- The **timestamp** is in **UNIX epoch format** (seconds since Jan 1st, 1970).
- Hostnames are simple identifiers like `host22`, `host29`.

---

## ⚙️ Assumptions

- **Connections are bidirectional in Task 1 (not in Task 2).**  
  `host22 host29` means both hosts were involved in a connection.
  Therefore, the parser checks both columns: source and destination.

- **Malformed lines** are skipped (e.g. missing fields, invalid timestamp).

- **Time ranges are inclusive**:  
  A timestamp exactly equal to the start or end time will be considered.

---

## 🚀 Usage

### Task 1 - Run from CLI

```bash
python main.py <logfile> <host> "<start_time>" "<end_time>"
```

### Example

```bash
python main.py data/Optional-connections.log host22 "2024-01-01 00:00:00" "2024-12-30 23:59:59"
```

### Output

Hosts connected to 'host22' between 2024-01-01 00:00:00 and 2024-12-30 23:59:59:
- host29
- host35

### Task 2 - Batch Mode

```bash
python stream.py \
  --logfile data/Optional-connections.log \
  --incoming host22 \
  --outgoing host22 \
  --frequency 31536000
```
--incoming: show who connected **to** this host

--outgoing: show who this host connected **to**

--frequency: time window in **seconds**


### Example Output

```bash
📊 Report at 2025-05-26T18:57:46+00:00:

🔻 Hosts connected TO 'host22':
- host29
- host10
...

🔺 Hosts 'host22' connected TO:
- host1
- host2
...

🏆 Host with most connections: host80 (144 connections)
```

## 🧪 Run Tests

Currently, only Task 1 has test coverage:

```bash
make test
```

Test file: 
- `tests/test_parser.py`


## 🛠️ Makefile Commands

```bash
make install       # Install dependencies from requirements.txt
make freeze        # Freeze current environment to requirements.txt
make test          # Run all unit tests (currently only Task 1)
make run-task1     # Run Task 1 with example arguments
make run-task2     # Run Task 2 in batch mode with example arguments
make clean         # Remove __pycache__ and .pyc files
```


## 📦 Dependencies

Install them with:

```bash
make install
```

Freeze to requirements.txt:

```bash
make freeze
```

Currently only pytest is required

## 📁 Project Structure

```plaintext
clarity-log-parser/
├── src/
│   ├── parser.py           # Task 1 core logic
│   └── stream_monitor.py   # Task 2 core logic (batch mode)
├── stream.py               # Task 2 CLI (batch)
├── main.py                 # Task 1 CLI
├── tests/
│   └── test_parser.py      # Tests for Task 1
├── data/                   # Sample log files
├── requirements.txt
├── Makefile
└── README.md
```
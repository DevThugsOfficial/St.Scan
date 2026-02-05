import serial
import pandas as pd
import os
import csv
from datetime import datetime
from pathlib import Path

# -----------------------------
# Arduino serial configuration
# -----------------------------
BAUD_RATE = 9600
# ensure we read/write the CSV inside the database folder (same file the GUI uses)
csv_file = str(Path(__file__).resolve().parent / "Students_Data.csv")

# CSV columns
columns = ['ID', 'Name', 'Status', 'ClassesAttended', 'TimeIn', 'TimeOut', 'Img_Path']

# -----------------------------
# Initialize CSV if missing
# -----------------------------
if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)

print("Waiting for RFID scans... (Press Ctrl+C to stop)")

# -----------------------------
# Helper functions
# -----------------------------
def format_student_id(number: int) -> str:
    """Format student ID as 00-001, 00-002, etc."""
    return f"00-{int(number):03d}"

def get_image_path(name: str) -> str:
    """Generate image path from name (replace spaces with nothing, default jpeg)."""
    filename = name.replace(" ", "") + ".jpeg"
    return f"assets/profiles/{filename}"

def find_serial_port():
    """Attempt to detect Arduino/RFID serial port automatically."""
    # Prefer stable by-id paths
    by_id_path = "/dev/serial/by-id"
    if os.path.exists(by_id_path):
        devices = os.listdir(by_id_path)
        if devices:
            return os.path.join(by_id_path, devices[0])

    # Fallbacks
    for port in ["/dev/ttyACM0", "/dev/ttyUSB0"]:
        if os.path.exists(port):
            return port

    return None

def _now_str() -> str:
    """Return portable time string like '4:32 PM'."""
    return datetime.now().strftime("%I:%M %p").lstrip("0")


def _upsert_scan(student_id: str, name: str, status: str) -> None:
    """
    Insert or update a student row in Students_Data.csv for a scan event.
    Behavior:
    - If student row does not exist: add new row. If status == 'Present' set TimeIn and ClassesAttended appropriately.
    - If student row exists and TimeIn is empty: set TimeIn (first scan).
    - If student row exists and TimeIn exists but TimeOut empty (or on subsequent scans): set/update TimeOut.
    - ClassesAttended is incremented only when setting TimeIn for a Present status.
    """
    # ensure file exists and read current rows
    rows = []
    if os.path.exists(csv_file):
        try:
            with open(csv_file, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [r for r in reader]
        except Exception as e:
            print(f"Error reading CSV in _upsert_scan: {e}")
            rows = []

    now = _now_str()
    status_norm = (status or "").strip().capitalize()
    written = False

    for r in rows:
        if r.get("ID", "").strip() == student_id:
            # existing student
            time_in = (r.get("TimeIn") or "").strip()
            time_out = (r.get("TimeOut") or "").strip()

            if not time_in:
                # first scan -> set TimeIn, update Status, increment ClassesAttended if Present
                r["TimeIn"] = now
                r["Status"] = status_norm
                try:
                    ca = int(r.get("ClassesAttended") or 0)
                except Exception:
                    ca = 0
                if status_norm.lower() == "present":
                    ca += 1
                r["ClassesAttended"] = str(ca)
            else:
                # subsequent scan -> record/update TimeOut
                r["TimeOut"] = now
                # Do not change ClassesAttended on TimeOut
                # Optionally update status to remain as-is
            written = True
            break

    if not written:
        # New student row
        img = ""
        try:
            img = get_image_path(name)
        except Exception:
            img = ""
        new_row = {
            "ID": student_id,
            "Name": name,
            "Status": status_norm,
            "ClassesAttended": "1" if status_norm.lower() == "present" else "0",
            "TimeIn": now if status_norm.lower() == "present" else "",
            "TimeOut": "" if status_norm.lower() == "present" else "",
            "Img_Path": img,
        }
        rows.append(new_row)

    # write back safely
    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["ID", "Name", "Status", "ClassesAttended", "TimeIn", "TimeOut", "Img_Path"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k, "") for k in fieldnames})
    except Exception as e:
        print(f"Error writing CSV in _upsert_scan: {e}")

# -----------------------------
# Connect to Arduino
# -----------------------------
SERIAL_PORT = find_serial_port()

if not SERIAL_PORT:
    print("No Arduino/RFID device detected.")
    print("Please plug in the device and restart the app.")
    exit(1)

print(f"Using serial port: {SERIAL_PORT}")

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
except serial.SerialException as e:
    print(f"Error connecting to {SERIAL_PORT}: {e}")
    exit(1)

# -----------------------------
# Main loop
# -----------------------------
while True:
    try:
        ser.reset_input_buffer()
        rfid_line = ser.readline().decode(errors='ignore').strip()  # safely decode

        if rfid_line:
            try:
                name, number, status = [x.strip() for x in rfid_line.split(",")]
            except ValueError:
                print(f"Bad line received: {rfid_line}")
                continue

            student_id = format_student_id(number)

            _upsert_scan(student_id, name, status)

            # Console feedback
            print(f"{name} ({student_id}) -> {status}")

    except KeyboardInterrupt:
        print("\nExiting...")
        break
    except Exception as e:
        print(f"Unexpected error: {e}")

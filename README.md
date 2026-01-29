# Attendance Checker Management System (AMS)

A desktop-based Attendance Checker Management System designed for teachers (admin only) using Arduino RFID, Python, and MySQL Database. The system automatically records attendance using RFID scanning and provides an admin dashboard for student management and reporting.

---

## 🚀 Features

- Admin (Teacher) Login System
- Student Management (CRUD Operations)
- RFID-based Attendance Recording
- Arduino USB Serial Communication
- MySQL Database Integration
- Attendance Reports Export (CSV)
- Real-time Attendance Monitoring
- Secure Password Hashing
- Desktop Dashboard Interface

---

## 🛠 Technologies Used

- Python 3
- Arduino (RFID Module)
- MySQL Database
- PySerial
- Tkinter (UI)
- MySQL Connector

---

## 📂 Project Structure

```
AMS/
├── main.py
├── auth/
├── dashboard/
├── core/
├── arduino/
├── database/
├── ui/
├── services/
├── utils/
├── assets/
└── logs/
```

---

## 🔧 System Requirements

- Python 3.8+
- Arduino UNO / ESP32
- RFID RC522 Module
- MySQL Server
- USB Cable
- Linux / Windows OS

---

## 📦 Install Dependencies

Create virtual environment (optional):

```
python3 -m venv venv
source venv/bin/activate
```

Install packages:

```
pip install pyserial mysql-connector-python
```

---

## ⚙ Database Setup

1. Open MySQL:

```
mysql -u root -p
```

2. Create database:

```
CREATE DATABASE attendance_system;
```

3. Update credentials:

Edit file:

```
database/db_config.py
```

---

## ▶ Running The System

Start the application:

```
python main.py
```

---

## 📡 System Workflow

1. Admin logs in
2. Teacher opens dashboard
3. Student taps RFID card
4. Arduino reads UID
5. Python receives data
6. Attendance saved to MySQL
7. Record displayed in dashboard

---

## 👨‍🏫 User Role

This system supports only ONE role:

- Admin (Teacher)

The admin can:

- Manage students
- View attendance
- Export reports
- Monitor real-time scans

---

## 📈 Future Enhancements

- Face Recognition Login
- Cloud Database Sync
- Mobile App Integration
- QR Code Attendance Backup
- Analytics Dashboard
- Automatic Email Reports

---

## 📜 License

This project is for educational and academic purposes.

---

## ✨ Author

Developed by: DevThugs Company  
Course: Computer Science / Embedded Systems  

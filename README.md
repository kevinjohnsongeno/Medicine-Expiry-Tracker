# Medicine Expiry Tracker

A lightweight, Command Line Interface (CLI) application built with **Python** and **MySQL**. It enables healthcare providers, small pharmacies or individual users to systematically manage medicine stock, monitor shelf life using SQL logic, and receive native desktop notifications for expired pharmaceutical products.

---

## Features

- **Inventory Input Validation:** Add new medicines securely with strict data formatting and automatic parsing for expiry dates (`DD-MM-YYYY`).
- **Structural Terminal UI:** Displays structured inventories dynamically inside the terminal with robust alignment padding (`<20`, `<15`).
- **Dynamic Real-time Statuses:** Automatically tracks chronological safety margins using conditional database matrix evaluation:
  - `Expired`: Item's shelf life has ended.
  - `Expires Today`: Expiry exactly matches the client host machine's system date.
  - `Expires Soon`: Items entering critical expiration window (within the next 7 days).
  - `OK`: Safe inventory status with viable commercial buffers.
- **Custom Threshold Projections:** Query and filter future-critical items by passing custom parameters.
- **Background Service Interactivity:** Leverages cross-platform hooks to deliver push alerts for items flagged as expired.

---

## System Architecture & Schema Definition

The application follows a standard database-client architecture. Data persistence is decoupled from client runtimes, leveraging index-optimized fields inside an enterprise-grade relation manager (MySQL).

### Requirements & Platform Support
- **Python Runtime:** Version `3.8` or newer.
- **Database Engine:** MySQL Server Community/Enterprise `8.0+`.

### Database Init Script
Run the following structure inside your local database terminal or workbench client before running the script:

```sql
-- 1. Initialize Schema Container
CREATE DATABASE IF NOT EXISTS medicine_tracker
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE medicine_tracker;

-- 2. Construct Core Metrics Table
CREATE TABLE IF NOT EXISTS medicinedetails (
    medicine_id INT AUTO_INCREMENT UNIQUE COMMENT 'Internal Tracking Matrix Index',
    name VARCHAR(255) NOT NULL COMMENT 'Commercial / Generic Name',
    dosage VARCHAR(100) DEFAULT NULL COMMENT 'Volume Spec (e.g., 500mg, 10ml)',
    schedule_times VARCHAR(255) DEFAULT NULL COMMENT 'Usage cadence metadata',
    expiry_date DATE NOT NULL COMMENT 'Calculated Expiration Timestamp',
    quantity INT NOT NULL DEFAULT 0 COMMENT 'Active Inventory Metrics',
    PRIMARY KEY (medicine_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

```
# Deployment & Setup Blueprint

## 1. Runtime Isolation & Package Delivery

Install the required dependencies inside your virtual environment:

```bash
pip install mysql-connector-python plyer
```

---

## 2. Runtime Authentication Matrix

Locate the database configuration block at the end of your `main.py` file and update it with your local MySQL credentials:

```python
# System Database Bridge Configuration
connection = mysql.connector.connect(
    host="127.0.0.1",         # Host Server Loopback Address
    port=3306,                # Default MySQL Port
    user="your_username",     # MySQL Username
    password="your_password", # MySQL Password
    database="medicine_tracker"
)
```

---

# Active Operation Manual

Run the application using:

```bash
python main.py
```

---

# CLI Menu Preview Reference

After successful execution, the terminal interface displays:

```plaintext
Successfully connected to the database ✅

Menu
1. Add Medicine
2. View All Medicines
3. Check Expired Medicines
4. Check Medicines About To Expire
5. Check Medicines with Status
6. Notify Expired Medicines
7. Exit

SELECT OPERATION:
```

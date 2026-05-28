from asyncio import timeout

import mysql.connector
from datetime import datetime
from plyer import notification
def add_medicine():
    name = input("Name:")
    dosage = input("Dosage:")
    schedule = input("Schedule:")
    expiry = input("Expiry Date(DD-MM-YYYY):")
    try:
        expiry = datetime.strptime(expiry,"%d-%m-%Y")
        expiry.strftime("%Y-%m-%d")
    except:
        print("⚠️ Wrong date format! Please use DD-MM-YYYY.")
        return
    quantity = input("Quantity:")
    query = '''INSERT INTO medicinedetails(name, dosage, schedule_times, expiry_date, quantity)
    VALUES(%s, %s, %s, %s, %s)'''
    values = (name, dosage, schedule, expiry, quantity)
    cursor.execute(query,values)
    connection.commit()
    print("✅ Medicine details added successfully!")

def view_medicines():
    query = '''SELECT * FROM medicinedetails'''
    cursor.execute(query)
    medicines = cursor.fetchall()
    if not medicines:
        print("⚠️ No medicines found.\n")
    else:
        print(f"{'ID':<5} {'Name':<20} {'Dosage':<10} {'Schedule':<15} {'Expiry Date':<12} {'Qty':<5}")
        print("-" * 70)
        for medicine in medicines:
            med_id, name, dosage, schedule, expiry, quantity = medicine
            print(f"{med_id:<5} {name:<20} {dosage:<10} {schedule:<15} {expiry:%Y-%m-%d}    {quantity:<5}")
        print()
def check_expired_medicines():
    query = '''SELECT * FROM medicinedetails WHERE expiry_date < CURDATE()'''
    cursor.execute(query)
    medicines = cursor.fetchall()
    print("Expired Medicines:\n")
    print(f"{'ID':<5} {'Name':<20} {'Dosage':<10} {'Schedule':<15} {'Expiry Date':<12} {'Qty':<5}")
    print("-" * 70)
    for medicine in medicines:
        med_id, name, dosage, schedule, expiry, quantity = medicine
        print(f"{med_id:<5} {name:<20} {dosage:<10} {schedule:<15} {expiry:%Y-%m-%d}    {quantity:<5}")
    print()
def check_medicines_to_be_expired():
    days = int(input("Days before the expiration:"))
    query = f'''SELECT medicine_id, name, dosage, schedule_times, expiry_date, quantity,
       GREATEST(DATEDIFF(expiry_date, CURDATE()),0) AS days_left FROM medicinedetails  WHERE DATEDIFF(expiry_date, CURDATE()) BETWEEN 1 AND {days} ORDER BY GREATEST(DATEDIFF(expiry_date, CURDATE()),0) ASC;'''
    cursor.execute(query)
    medicines = cursor.fetchall()
    print("Medicines about to be expired:\n")
    print(f"{'ID':<5} {'Name':<20} {'Dosage':<10} {'Schedule':<15} {'Expiry Date':<12} {'Qty':<5} {'Days Left':<10}")
    print("-" * 83)
    for med_id, name, dosage, schedule, expiry, quantity, days_left in medicines:
        print(f"{med_id:<5} {name:<20} {dosage:<10} {schedule:<15} {expiry:%Y-%m-%d}    {quantity:<5} {days_left:<10}")
    print()
def fetch_with_status():
    query = f'''
SELECT medicine_id, name, dosage, schedule_times, expiry_date, quantity,GREATEST(DATEDIFF(expiry_date, CURDATE()),0) AS days_left, CASE WHEN expiry_date < CURDATE() THEN 'Expired' WHEN expiry_date = CURDATE() THEN 'Expires Today' WHEN DATEDIFF(expiry_date, CURDATE()) BETWEEN 1 AND 7 THEN 'Expires Soon' ELSE 'OK' END AS status FROM medicinedetails
ORDER BY expiry_date ASC'''
    cursor.execute(query)
    medicines = cursor.fetchall()
    print(f"{'ID':<5} {'Name':<20} {'Dosage':<10} {'Schedule':<15} {'Expiry Date':<12} {'Qty':<5} {'Days Left':<10}  {'Status':<5}")
    print("-" * 93)
    for med_id, name, dosage, schedule, expiry, quantity, days_left,status in medicines:
        print(f"{med_id:<5} {name:<20} {dosage:<10} {schedule:<15} {expiry:%Y-%m-%d}    {quantity:<5} {days_left:<10}  {status:<20}")
    print()
def notify_expiry_medicines():
    query = '''SELECT name,expiry_date FROM medicinedetails WHERE expiry_date < curdate();'''
    cursor.execute(query)
    medicines = cursor.fetchall()
    for name,expiry in medicines:
        notification.notify(
        title = "⚠️Expired Medicine Alert",
            message = f"{name} expired on {expiry:%d-%m-%Y}",
            timeout = 5
        )
connection = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "password",
    database = "medicine_tracker")
cursor = connection.cursor()
if connection.is_connected():
    print("Successfully connected to the database ✅")
else:
    print("❌ Connection to the database failed")
while True:
    print("Menu")
    ch = input("1. Add Medicine\n2. View All Medicines\n3. Check Expired Medicines\n4. Check Medicines About To Expire\n5. Check Medicines with Status\n6. Notify Expired Medicines\n7. Exit\nSELECT OPERATION:")
    if ch == '1':
        add_medicine()
    elif ch == '2':
        view_medicines()
    elif ch == '3':
        check_expired_medicines()
    elif ch == '4':
        check_medicines_to_be_expired()
    elif ch == '5':
        fetch_with_status()
    elif ch == '6':
        notify_expiry_medicines()
    elif ch == '7':
        print("Exiting...")
        break
    else:
        print("\nPlease enter a number from 1 - 6.\n")
cursor.close()
connection.close()

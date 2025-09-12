import mysql.connector as sql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")  # Example: railway_management

# Connect to MySQL
conn = sql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, database=DB_NAME)
cur = conn.cursor()

# Create tables if not exist
cur.execute("""
CREATE TABLE IF NOT EXISTS customer_data (
    cust_no INT PRIMARY KEY,
    cust_name VARCHAR(50),
    address VARCHAR(150),
    journey_date DATE,
    source VARCHAR(50),
    destination VARCHAR(50)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS ticket_data (
    cust_no INT PRIMARY KEY,
    ticket_price INT,
    luggage_charge INT,
    total_bill INT,
    FOREIGN KEY (cust_no) REFERENCES customer_data(cust_no)
)
""")
conn.commit()

# Functions
def register_customer():
    cust_no = int(input("Enter Customer Number: "))
    name = input("Enter Name: ").upper()
    addr = input("Enter Address: ").upper()
    journey_date = input("Enter Date of Journey (YYYY-MM-DD): ")
    source = input("Enter Source: ").upper()
    destination = input("Enter Destination: ").upper()

    cur.execute("INSERT INTO customer_data VALUES (%s,%s,%s,%s,%s,%s)",
                (cust_no, name, addr, journey_date, source, destination))
    conn.commit()
    print("Customer registered successfully.")

def book_ticket():
    cust_no = int(input("Enter Customer Number: "))
    print("Ticket types:\n1. First Class - 6000\n2. Business Class - 4000\n3. Economy - 2000")
    type_choice = int(input("Choose ticket type: "))
    passengers = int(input("Enter number of passengers: "))

    if type_choice == 1:
        price = 6000 * passengers
    elif type_choice == 2:
        price = 4000 * passengers
    elif type_choice == 3:
        price = 2000 * passengers
    else:
        print("Invalid choice.")
        return

    luggage = int(input("Enter extra luggage weight (kg): "))
    luggage_charge = luggage * 100
    total = price + luggage_charge

    cur.execute("INSERT INTO ticket_data VALUES (%s,%s,%s,%s)",
                (cust_no, price, luggage_charge, total))
    conn.commit()
    print(f"Ticket booked. Total bill: {total}")

def display_customer():
    cust_no = int(input("Enter Customer Number to view details: "))
    cur.execute("""
    SELECT c.cust_no, c.cust_name, c.address, c.source, c.destination,
           t.ticket_price, t.luggage_charge, t.total_bill
    FROM customer_data c
    JOIN ticket_data t ON c.cust_no = t.cust_no
    WHERE c.cust_no = %s
    """, (cust_no,))
    data = cur.fetchall()
    if data:
        for row in data:
            print(f"Customer No: {row[0]}, Name: {row[1]}, Address: {row[2]}, Source: {row[3]}, Destination: {row[4]}, Ticket Price: {row[5]}, Luggage Charge: {row[6]}, Total: {row[7]}")
    else:
        print("No data found.")

def display_all_customers():
    cur.execute("""
    SELECT c.cust_no, c.cust_name, c.address, c.source, c.destination,
           t.ticket_price, t.luggage_charge, t.total_bill
    FROM customer_data c
    JOIN ticket_data t ON c.cust_no = t.cust_no
    """)
    data = cur.fetchall()
    for row in data:
        print(f"Customer No: {row[0]}, Name: {row[1]}, Address: {row[2]}, Source: {row[3]}, Destination: {row[4]}, Ticket Price: {row[5]}, Luggage Charge: {row[6]}, Total: {row[7]}")

# Menu Loop
while True:
    print("\n=== Railway Management System ===")
    print("1. Register Customer")
    print("2. Book Ticket")
    print("3. Display Customer Details")
    print("4. Display All Customers")
    print("5. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        register_customer()
    elif choice == 2:
        book_ticket()
    elif choice == 3:
        display_customer()
    elif choice == 4:
        display_all_customers()
    elif choice == 5:
        print("Exiting...")
        break
    else:
        print("Invalid choice. Try again.")

conn.close()

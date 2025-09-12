import mysql.connector as sql
import os

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "root"   # change to your MySQL password
DB_NAME = "dental_management_system"

# Connect to database
conn = sql.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_PASS,
    database=DB_NAME
)
cur = conn.cursor()

# Application Menu
def main_menu():
    while True:
        print("\n--- Dental Management System ---")
        print("1. Add Patient Record")
        print("2. View Patient Records")
        print("3. Add Employee Salary Record")
        print("4. View Employee Salary Records")
        print("5. Delete Patient Record")
        print("0. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            add_salary()
        elif choice == "4":
            view_salaries()
        elif choice == "5":
            delete_patient()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

# CRUD Functions
def add_patient():
    name = input("Patient Name: ").upper()
    age = int(input("Age: "))
    doctor = input("Doctor Consulted: ").upper()
    address = input("Address: ").upper()
    phone = int(input("Phone Number: "))
    cur.execute(
        "INSERT INTO patient_record (Patient_Name, Age, Doctor_Conculted, Address, Phone_Number) VALUES (%s, %s, %s, %s, %s)",
        (name, age, doctor, address, phone)
    )
    conn.commit()
    print("Patient record added successfully!")

def view_patients():
    cur.execute("SELECT * FROM patient_record")
    data = cur.fetchall()
    if data:
        for row in data:
            print(f"\nName: {row[0]}, Age: {row[1]}, Doctor: {row[2]}, Address: {row[3]}, Phone: {row[4]}")
    else:
        print("No patient records found.")

def add_salary():
    name = input("Employee Name: ").upper()
    profession = input("Profession: ").upper()
    salary = float(input("Salary Amount: "))
    address = input("Address: ").upper()
    phone = int(input("Phone Number: "))
    cur.execute(
        "INSERT INTO salary_record (Employee_Name, Proffession, Salary_Amount, Address, Phone_Number) VALUES (%s, %s, %s, %s, %s)",
        (name, profession, salary, address, phone)
    )
    conn.commit()
    print("Salary record added successfully!")

def view_salaries():
    cur.execute("SELECT * FROM salary_record")
    data = cur.fetchall()
    if data:
        for row in data:
            print(f"\nEmployee: {row[0]}, Profession: {row[1]}, Salary: {row[2]}, Address: {row[3]}, Phone: {row[4]}")
    else:
        print("No salary records found.")

def delete_patient():
    name = input("Enter patient name to delete: ").upper()
    cur.execute("DELETE FROM patient_record WHERE Patient_Name = %s", (name,))
    conn.commit()
    print("Patient record deleted successfully!")

# Run the application
if __name__ == "__main__":
    main_menu()
    conn.close()

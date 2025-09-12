# app.py - Computer Institute Management System
import mysql.connector as sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
conn = sql.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_PASS,
    database=DB_NAME
)
cur = conn.cursor()

# Function to enroll a student
def enroll_student():
    adm_no = int(input("Enter Admission Number: "))
    name = input("Enter Candidate Name: ").title()
    course = input("Enter Course (JAVA/Python/C/BASIC/HTML): ").upper()
    cur.execute("INSERT INTO candidate_details VALUES (%s, %s, %s)", (adm_no, name, course))
    conn.commit()
    print(f"Enrollment successful for {name} in {course} course!\n")

# Function to edit enrollment (admin only)
def edit_enrollment():
    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")
    if username == "admin" and password == "123":  # You can change credentials
        print("\n1. Delete Enrollment\n2. Edit Name\n3. Edit Course")
        option = int(input("Choose an option: "))
        if option == 1:
            adm_no = int(input("Enter Admission Number to delete: "))
            cur.execute("DELETE FROM candidate_details WHERE adm_no = %s", (adm_no,))
            conn.commit()
            print("Enrollment deleted successfully!\n")
        elif option == 2:
            adm_no = int(input("Enter Admission Number to edit name: "))
            new_name = input("Enter new name: ").title()
            cur.execute("UPDATE candidate_details SET candidate_name=%s WHERE adm_no=%s", (new_name, adm_no))
            conn.commit()
            print("Name updated successfully!\n")
        elif option == 3:
            adm_no = int(input("Enter Admission Number to edit course: "))
            new_course = input("Enter new course: ").upper()
            cur.execute("UPDATE candidate_details SET course_select=%s WHERE adm_no=%s", (new_course, adm_no))
            conn.commit()
            print("Course updated successfully!\n")
        else:
            print("Invalid option!\n")
    else:
        print("Invalid admin credentials!\n")

# Function to display all enrollments
def display_all():
    cur.execute("SELECT * FROM candidate_details")
    data = cur.fetchall()
    if data:
        print("\n--- Candidate Details ---")
        for row in data:
            print(f"Admission Number: {row[0]}, Name: {row[1]}, Course: {row[2]}")
        print()
    else:
        print("No records found!\n")

# Main menu loop
def main_menu():
    while True:
        print("==== SSA Computer Institute Management System ====")
        print("1. Enroll Student")
        print("2. Edit Enrollment (Admin)")
        print("3. Display All Candidates")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            enroll_student()
        elif choice == "2":
            edit_enrollment()
        elif choice == "3":
            display_all()
        elif choice == "4":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.\n")

# Run the program
if __name__ == "__main__":
    main_menu()
    conn.close()

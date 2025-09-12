import gradio as gr
import mysql.connector as sql

# Database connection
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "root"  # change if needed
DB_NAME = "dental_management_system"

conn = sql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, database=DB_NAME)
cur = conn.cursor()

# Add Patient Record
def add_patient(name, age, doctor, address, phone):
    cur.execute(
        "INSERT INTO patient_record (Patient_Name, Age, Doctor_Conculted, Address, Phone_Number) VALUES (%s, %s, %s, %s, %s)",
        (name.upper(), int(age), doctor.upper(), address.upper(), int(phone))
    )
    conn.commit()
    return f"Patient {name} added successfully!"

# View All Patients
def view_patients():
    cur.execute("SELECT * FROM patient_record")
    data = cur.fetchall()
    if not data:
        return "No patient records found."
    result = ""
    for row in data:
        result += f"Name: {row[0]}, Age: {row[1]}, Doctor: {row[2]}, Address: {row[3]}, Phone: {row[4]}\n"
    return result

# Delete Patient Record
def delete_patient(name):
    cur.execute("DELETE FROM patient_record WHERE Patient_Name = %s", (name.upper(),))
    conn.commit()
    return f"Patient {name} deleted successfully!"

# Add Employee Salary Record
def add_salary(name, profession, salary, address, phone):
    cur.execute(
        "INSERT INTO salary_record (Employee_Name, Proffession, Salary_Amount, Address, Phone_Number) VALUES (%s, %s, %s, %s, %s)",
        (name.upper(), profession.upper(), float(salary), address.upper(), int(phone))
    )
    conn.commit()
    return f"Employee {name}'s salary record added successfully!"

# View Employee Salaries
def view_salaries():
    cur.execute("SELECT * FROM salary_record")
    data = cur.fetchall()
    if not data:
        return "No salary records found."
    result = ""
    for row in data:
        result += f"Employee: {row[0]}, Profession: {row[1]}, Salary: {row[2]}, Address: {row[3]}, Phone: {row[4]}\n"
    return result

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## Dental Management System Web Interface")
    
    with gr.Tab("Add Patient"):
        name = gr.Textbox(label="Name")
        age = gr.Number(label="Age")
        doctor = gr.Textbox(label="Doctor Consulted")
        address = gr.Textbox(label="Address")
        phone = gr.Textbox(label="Phone Number")
        btn_add_patient = gr.Button("Add Patient")
        output_add_patient = gr.Textbox()
        btn_add_patient.click(add_patient, inputs=[name, age, doctor, address, phone], outputs=output_add_patient)
    
    with gr.Tab("View Patients"):
        btn_view_patients = gr.Button("View All Patients")
        output_view_patients = gr.Textbox()
        btn_view_patients.click(view_patients, outputs=output_view_patients)
    
    with gr.Tab("Delete Patient"):
        name_del = gr.Textbox(label="Patient Name to Delete")
        btn_del_patient = gr.Button("Delete Patient")
        output_del_patient = gr.Textbox()
        btn_del_patient.click(delete_patient, inputs=name_del, outputs=output_del_patient)
    
    with gr.Tab("Add Salary Record"):
        emp_name = gr.Textbox(label="Employee Name")
        profession = gr.Textbox(label="Profession")
        salary = gr.Number(label="Salary Amount")
        emp_address = gr.Textbox(label="Address")
        emp_phone = gr.Textbox(label="Phone Number")
        btn_add_salary = gr.Button("Add Salary Record")
        output_add_salary = gr.Textbox()
        btn_add_salary.click(add_salary, inputs=[emp_name, profession, salary, emp_address, emp_phone], outputs=output_add_salary)
    
    with gr.Tab("View Salaries"):
        btn_view_salary = gr.Button("View All Salaries")
        output_view_salary = gr.Textbox()
        btn_view_salary.click(view_salaries, outputs=output_view_salary)

demo.launch()

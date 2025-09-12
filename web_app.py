import gradio as gr
import mysql.connector as sql
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

# ---------- DATABASE CONNECTION FUNCTIONS ----------
def connect_db(db_name):
    return sql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, database=db_name)

# ---------- COMPUTER INSTITUTE ----------
def enroll_student(adm_no, name, course):
    conn = connect_db("cims")
    c = conn.cursor()
    c.execute("INSERT INTO candidate_details VALUES (%s, %s, %s)", (adm_no, name, course))
    conn.commit()
    conn.close()
    return f"{name} enrolled for {course}!"

def show_students():
    conn = connect_db("cims")
    c = conn.cursor()
    c.execute("SELECT * FROM candidate_details")
    data = c.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Admission No", "Name", "Course"])

# ---------- DENTAL CLINIC ----------
def add_patient(name, age, doctor, address, phone):
    conn = connect_db("dental_management_system")
    c = conn.cursor()
    c.execute("INSERT INTO patient_record VALUES (%s, %s, %s, %s, %s)", 
              (name, age, doctor, address, phone))
    conn.commit()
    conn.close()
    return f"Patient {name} added successfully!"

def view_patients():
    conn = connect_db("dental_management_system")
    c = conn.cursor()
    c.execute("SELECT * FROM patient_record")
    data = c.fetchall()
    conn.close()
    return pd.DataFrame(data, columns=["Name", "Age", "Doctor", "Address", "Phone"])

# ---------- RAILWAY ----------
def register_customer(custno, name, addr, jr_date, source, dest):
    conn = connect_db("railway")
    c = conn.cursor()
    c.execute("INSERT INTO pdata VALUES (%s, %s, %s, %s, %s, %s)", 
              (custno, name, addr, jr_date, source, dest))
    conn.commit()
    conn.close()
    return f"Customer {name} registered successfully!"

def ticket_price(custno, cls, passengers, luggage):
    price = {"First": 6000, "Business": 4000, "Economy": 2000}
    tkt_charge = price[cls] * passengers
    lug_charge = luggage * 100
    total = tkt_charge + lug_charge
    
    conn = connect_db("railway")
    c = conn.cursor()
    c.execute("INSERT INTO tkt (custno, tkt_tot, lug_tot, g_tot) VALUES (%s,%s,%s,%s)", 
              (custno, tkt_charge, lug_charge, total))
    conn.commit()
    conn.close()
    return f"Total ticket price: {total} Rs"

# ---------- GRADIO INTERFACE ----------
with gr.Blocks() as demo:
    with gr.Tab("Computer Institute"):
        gr.Markdown("### Enroll Student")
        adm_no = gr.Number(label="Admission No")
        name = gr.Textbox(label="Name")
        course = gr.Dropdown(["JAVA","Python","C","BASIC","HTML"], label="Course")
        enroll_btn = gr.Button("Enroll")
        enroll_output = gr.Textbox(label="Output")
        enroll_btn.click(enroll_student, inputs=[adm_no, name, course], outputs=enroll_output)
        show_btn = gr.Button("Show All Students")
        show_output = gr.Dataframe()
        show_btn.click(show_students, inputs=None, outputs=show_output)

    with gr.Tab("Dental Clinic"):
        gr.Markdown("### Add Patient")
        pname = gr.Textbox(label="Patient Name")
        age = gr.Number(label="Age")
        doctor = gr.Textbox(label="Doctor")
        address = gr.Textbox(label="Address")
        phone = gr.Number(label="Phone Number")
        add_btn = gr.Button("Add Patient")
        add_output = gr.Textbox(label="Output")
        add_btn.click(add_patient, inputs=[pname, age, doctor, address, phone], outputs=add_output)
        view_btn = gr.Button("View Patients")
        view_output = gr.Dataframe()
        view_btn.click(view_patients, inputs=None, outputs=view_output)

    with gr.Tab("Railway"):
        gr.Markdown("### Register Customer")
        custno = gr.Number(label="Customer No")
        cname = gr.Textbox(label="Name")
        addr = gr.Textbox(label="Address")
        jr_date = gr.Textbox(label="Journey Date")
        source = gr.Textbox(label="Source")
        dest = gr.Textbox(label="Destination")
        reg_btn = gr.Button("Register")
        reg_output = gr.Textbox(label="Output")
        reg_btn.click(register_customer, inputs=[custno, cname, addr, jr_date, source, dest], outputs=reg_output)
        gr.Markdown("### Ticket Price")
        cls = gr.Dropdown(["First","Business","Economy"], label="Class")
        passengers = gr.Number(label="No. of Passengers")
        luggage = gr.Number(label="Extra Luggage (kg)")
        tkt_btn = gr.Button("Calculate Price")
        tkt_output = gr.Textbox(label="Output")
        tkt_btn.click(ticket_price, inputs=[custno, cls, passengers, luggage], outputs=tkt_output)

demo.launch()

import mysql.connector
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Connect to database
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_PASS,
    database=DB_NAME
)
cursor = conn.cursor()

# Functions
def enroll_student(adm_no, name, course):
    name = name.upper()
    course = course.upper()
    cursor.execute(
        "INSERT INTO candidate_details (adm_no, candidate_name, course_select) VALUES (%s, %s, %s)",
        (adm_no, name, course)
    )
    conn.commit()
    return f"{name} enrolled successfully for {course} course!"

def display_all_students():
    cursor.execute("SELECT * FROM candidate_details")
    rows = cursor.fetchall()
    if rows:
        result = ""
        for row in rows:
            result += f"Admission No: {row[0]}, Name: {row[1]}, Course: {row[2]}\n"
        return result
    return "No students enrolled yet."

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## SSA Computer Institute Management System")
    
    with gr.Tab("Enroll Student"):
        adm_no = gr.Number(label="Admission Number")
        name = gr.Textbox(label="Student Name")
        course = gr.Dropdown(["JAVA", "PYTHON", "C", "BASIC", "HTML"], label="Course")
        enroll_btn = gr.Button("Enroll")
        enroll_output = gr.Textbox(label="Output")
        enroll_btn.click(enroll_student, inputs=[adm_no, name, course], outputs=enroll_output)
    
    with gr.Tab("View All Students"):
        view_btn = gr.Button("Display All Students")
        view_output = gr.Textbox(label="All Students")
        view_btn.click(display_all_students, inputs=None, outputs=view_output)

demo.launch()

import mysql.connector as sql
import gradio as gr
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Connect to MySQL
conn = sql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, database=DB_NAME)
cur = conn.cursor()

# Function to register customer
def register_customer(custno, custname, addr, jrdate, source, destination):
    cur.execute(
        "INSERT INTO pdata VALUES (%s,%s,%s,%s,%s,%s)",
        (custno, custname, addr, jrdate, source, destination)
    )
    conn.commit()
    return f"Customer {custname} registered successfully!"

# Function to calculate ticket price
def calculate_ticket(custno, ticket_type, passengers, luggage_kg):
    price_map = {1: 6000, 2: 4000, 3: 2000}
    tkt_price = price_map.get(ticket_type, 0) * passengers
    luggage_price = luggage_kg * 100
    total = tkt_price + luggage_price
    cur.execute(
        "INSERT INTO tkt VALUES (%s,%s,%s,%s)",
        (custno, tkt_price, luggage_price, total)
    )
    conn.commit()
    return f"Total ticket price: {total}"

# Function to view customer details
def view_customer(custno):
    cur.execute(
        "SELECT pdata.custno, pdata.custname, pdata.addr, pdata.source, pdata.destination, tkt.tkt_tot, tkt.lug_tot, tkt.g_tot "
        "FROM pdata INNER JOIN tkt ON pdata.custno=tkt.custno WHERE pdata.custno=%s",
        (custno,)
    )
    data = cur.fetchall()
    if data:
        return pd.DataFrame(data, columns=["Customer No", "Name", "Address", "Source", "Destination", "Ticket", "Luggage", "Total"])
    else:
        return "Customer not found"

# Function to view all customers
def view_all_customers():
    cur.execute(
        "SELECT pdata.custno, pdata.custname, pdata.addr, pdata.source, pdata.destination, tkt.tkt_tot, tkt.lug_tot, tkt.g_tot "
        "FROM pdata INNER JOIN tkt ON pdata.custno=tkt.custno"
    )
    data = cur.fetchall()
    return pd.DataFrame(data, columns=["Customer No", "Name", "Address", "Source", "Destination", "Ticket", "Luggage", "Total"])

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Railway Management System")
    
    with gr.Tab("Register Customer"):
        custno = gr.Number(label="Customer No")
        custname = gr.Textbox(label="Name")
        addr = gr.Textbox(label="Address")
        jrdate = gr.Textbox(label="Journey Date (YYYY-MM-DD)")
        source = gr.Textbox(label="Source")
        destination = gr.Textbox(label="Destination")
        btn = gr.Button("Register")
        output = gr.Textbox()
        btn.click(register_customer, [custno, custname, addr, jrdate, source, destination], output)
    
    with gr.Tab("Ticket Booking"):
        custno2 = gr.Number(label="Customer No")
        ticket_type = gr.Dropdown([1, 2, 3], label="Ticket Type (1=First, 2=Business, 3=Economy)")
        passengers = gr.Number(label="Number of Passengers")
        luggage_kg = gr.Number(label="Extra Luggage (kg)")
        btn2 = gr.Button("Calculate Total")
        output2 = gr.Textbox()
        btn2.click(calculate_ticket, [custno2, ticket_type, passengers, luggage_kg], output2)
    
    with gr.Tab("View Customer"):
        custno3 = gr.Number(label="Customer No")
        btn3 = gr.Button("View Details")
        output3 = gr.Dataframe()
        btn3.click(view_customer, custno3, output3)
    
    with gr.Tab("View All Customers"):
        btn4 = gr.Button("Show All")
        output4 = gr.Dataframe()
        btn4.click(view_all_customers, None, output4)

demo.launch()

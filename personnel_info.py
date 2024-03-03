import io
import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3
import os
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog


# Main Window
window = tkinter.Tk()
window.title("Personnel Entry Form")
window.geometry("1250x680")
window.resizable(False, False)

# Main Frame
frame = tkinter.Frame(window)
frame.pack()

i = 0


# Function to select image file from os
# and display on form selected image
def upload_img():
    global img_label
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Photo File", filetypes=(("JPG File", "*.jpg"),
                                                                                                        ("PNG File", "*.png"),
                                                                                                        ("All Files", "*.txt")))
    try:
        img_name = Image.open(filename)
        resized_photo = img_name.resize((300, 310))
        photo2 = ImageTk.PhotoImage(resized_photo)
        img_label.config(image=photo2)
        img_label = photo2
    except AttributeError:
        pass


def clear_image():
    global img_label
    img_label = Label(per_img_frame, image=photo)
    img_label.place(x=0, y=0)


# Function to collect personnel information into database
# and create one if one doesn't exist
def reg_per():
    if army_no_entry.get() == "" or rank_entry.get() == "" or first_name_entry.get() == "" or last_name_entry.get()\
       == "" or unit_entry.get() == "" or corps_entry.get() == "" or appointment_entry.get() == "" or deploy_entry.get()\
       == "" or state_entry.get() == "" or trade_entry.get() == "" or address_entry.get("1.0", 'end') == "":
        tkinter.messagebox.showinfo(title="ERROR", message="Please all fields are required to be filled")
    elif Gender_radio.get() == "":
        tkinter.messagebox.showerror(title="Error", message="Please select Gender")
    elif Marital_Status_radio.get() == "":
        tkinter.messagebox.showerror(title="Error", message="Please select Marital Status")
    else:
        # User Info
        try:
            with open(filename, 'rb') as file:
                photo_image = file.read()
        except NameError:
            pass
        army_number = army_no_entry.get()
        rank = rank_entry.get()
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        sex = Gender_radio.get()
        unit = unit_entry.get()
        corps = corps_entry.get()
        appointment = appointment_entry.get()
        deployment = deploy_entry.get()
        state = state_entry.get()
        trade = trade_entry.get()
        address = address_entry.get("1.0", 'end-1c')
        marital_status = Marital_Status_radio.get()
        try:
            image = photo_image
        except NameError:
            image = ""

        # Create Table
        conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Personnel_Info (serial INTEGER PRIMARY KEY AUTOINCREMENT, armynumber TEXT, 
        rank TEXT, firstname TEXT, lastname TEXT, sex TEXT, unit TEXT, corps TEXT, appointment TEXT, deployment TEXT, state TEXT, 
        trade TEXT, address TEXT, maritalstatus TEXT, image BLOB)
        '''
        conn.execute(table_create_query)

        # Insert Data
        data_insert_query = '''INSERT INTO Personnel_Info (armynumber, rank, firstname, lastname, sex, unit, corps, appointment,
        deployment, state, trade, address, maritalstatus, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (army_number, rank, firstname, lastname, sex, unit, corps, appointment, deployment, state, trade,
                             address, marital_status, image,)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        cursor.close()
        conn.close()

        # Notify info entry success
        tkinter.messagebox.showinfo(title="DONE", message="Personnel has been registered successfully")

        # Clear fields
        clear_all_fields()
        return


# Function to clear all input fields at will
def clear_all_fields():
    global img_label
    army_no_entry.delete(0, 'end')
    rank_entry.set('')
    first_name_entry.delete(0, 'end')
    last_name_entry.delete(0, 'end')
    unit_entry.delete(0, 'end')
    corps_entry.delete(0, 'end')
    appointment_entry.delete(0, 'end')
    deploy_entry.delete(0, 'end')
    state_entry.set('')
    trade_entry.delete(0, 'end')
    address_entry.delete('1.0', 'end')
    img_label = Label(per_img_frame, image=photo)
    img_label.place(x=0, y=0)
    return


# Function to return to DB Hub (close dialog box at the moment)
def go_back():
    window.destroy()
    pass


# ################### Command to start to view database on form ##################
def peruse_database():
    global img_label
    global i
    global blob_image
    clear_all_fields()
    upload_image_btn.config(state='disabled')
    clear_image_btn.config(state='disabled')
    clear_button.config(state='disabled')
    register_personnel_btn.config(state='disabled')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    c = cursor.execute("SELECT * FROM Personnel_Info")
    r = c.fetchall()

    Serial_Number.set(r[i][0])
    Army_Number.set(r[i][1])
    Rank.set(r[i][2])
    First_Name.set(r[i][3])
    Last_Name.set(r[i][4])
    Gender_radio.set(r[i][5])
    Unit.set(r[i][6])
    Corps.set(r[i][7])
    Appointment.set(r[i][8])
    Deployment.set(r[i][9])
    State.set(r[i][10])
    Trade.set(r[i][11])
    address_entry.insert(INSERT, r[i][12])
    Marital_Status_radio.set(r[i][13])
    blob_image = r[i][14]
    blob = io.BytesIO(r[i][14])
    image = Image.open(blob)
    resized_photo = image.resize((300, 310))
    per_image = ImageTk.PhotoImage(resized_photo)
    img_label.config(image=per_image)
    img_label = per_image

    cursor.close()
    conn.close()
    return


def next_personnel():
    global i
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    c = cursor.execute("SELECT COUNT(*) FROM Personnel_Info")
    result = c.fetchone()
    total = result[0]
    if Army_Number.get() == "":
        return
    if i == total - 1:
        tkinter.messagebox.showinfo("End", "Last Personnel in DB")
    else:
        i += 1
        peruse_database()
    cursor.close()
    conn.close()
    return


def previous_personnel():
    global i
    if Army_Number.get() == "":
        return 
    if i == 0:
        tkinter.messagebox.showinfo("Begin", "First Personnel in DB")
    else:
        i -= 1
        peruse_database()
    return


# ##################### Update Record ###################################
def update_record():
    if army_no_entry.get() == "" or rank_entry.get() == "" or first_name_entry.get() == "" or last_name_entry.get()\
       == "" or unit_entry.get() == "" or corps_entry.get() == "" or appointment_entry.get() == "" or deploy_entry.get()\
       == "" or state_entry.get() == "" or trade_entry.get() == "" or address_entry.get("1.0", 'end') == "":
        tkinter.messagebox.showinfo(title="ERROR", message="Please all fields are required to be filled")
    elif Gender_radio.get() == "":
        tkinter.messagebox.showerror(title="Error", message="Please select Gender")
    elif Marital_Status_radio.get() == "":
        tkinter.messagebox.showerror(title="Error", message="Please select Marital Status")
    else:
        # User Info
        serial = Serial_Number.get()
        army_number = Army_Number.get()
        rank = Rank.get()
        firstname = First_Name.get()
        lastname = Last_Name.get()
        sex = Gender_radio.get()
        unit = Unit.get()
        corps = Corps.get()
        appointment = Appointment.get()
        deployment = Deployment.get()
        state = State.get()
        trade = Trade.get()
        address = address_entry.get("1.0", 'end-1c')
        marital_status = Marital_Status_radio.get()
        try:
            image = blob_image
        except NameError:
            image = ""

        # Connect to database
        conn = sqlite3.connect('data.db')

        # Edit Data
        data_update_query = ("UPDATE Personnel_Info SET armynumber = ?, rank = ?, firstname = ?, lastname = ?, sex = ?, unit = ?,\
                       corps = ?, appointment = ?, deployment = ?, state = ?, trade = ?, address = ?, maritalstatus = ?,\
                       image = ? WHERE serial = ?")
        data_update_tuple = (army_number, rank, firstname, lastname, sex, unit, corps, appointment, deployment, state,
                             trade, address, marital_status, image, serial)
        cursor = conn.cursor()
        cursor.execute(data_update_query, data_update_tuple)
        conn.commit()
        cursor.close()
        conn.close()

        # Notify info entry success
        tkinter.messagebox.showinfo(title="DONE", message="Personnel record updated successfully")

        # Clear fields
        clear_all_fields()
        return


# Frame to collect all required information
per_info_frame = tkinter.LabelFrame(frame, text="Personnel Information")
per_info_frame.grid(row=0, column=0)


# Labels and Entries
army_no_label = tkinter.Label(per_info_frame, text="Army Number")
army_no_label.grid(row=0, column=0)
Army_Number = StringVar()
army_no_entry = tkinter.Entry(per_info_frame, textvariable=Army_Number)
army_no_entry.grid(row=1, column=0)
rank_label = tkinter.Label(per_info_frame, text="Rank")
rank_label.grid(row=0, column=1)
Rank = StringVar()
rank_entry = ttk.Combobox(per_info_frame, values=["Brig Gen", "Col", "Lt Col", "Maj", "Capt", "Lt", "2Lt", "AWO", "MWO",
                                                  "WO", "SSgt", "Sgt", "Cpl", "LCpl", "Pte"], state="readonly", textvariable=Rank)
rank_entry.grid(row=1, column=1)
first_name_label = tkinter.Label(per_info_frame, text="First Name")
first_name_label.grid(row=0, column=2)
First_Name = StringVar()
first_name_entry = tkinter.Entry(per_info_frame, textvariable=First_Name)
first_name_entry.grid(row=1, column=2)
last_name_label = tkinter.Label(per_info_frame, text="Last Name")
last_name_label.grid(row=0, column=3)
Last_Name = StringVar()
last_name_entry = tkinter.Entry(per_info_frame, textvariable=Last_Name)
last_name_entry.grid(row=1, column=3)
unit_label = tkinter.Label(per_info_frame, text="Unit")
unit_label.grid(row=0, column=4)
Unit = StringVar()
unit_entry = tkinter.Entry(per_info_frame, textvariable=Unit)
unit_entry.grid(row=1, column=4)
gender_label = tkinter.Label(per_info_frame, text="Gender")
gender_label.grid(row=0, column=5)
Gender_radio = StringVar()
R1 = Radiobutton(per_info_frame, text="Male", variable=Gender_radio, value="Male")
R1.grid(row=1, column=5, sticky='w')
R2 = Radiobutton(per_info_frame, text="Female", variable=Gender_radio, value="Female")
R2.grid(row=2, column=5, sticky='w')
status_label = tkinter.Label(per_info_frame, text="Marital Status")
status_label.grid(row=0, column=6)
Marital_Status_radio = tkinter.StringVar()
R3 = Radiobutton(per_info_frame, text="Single", variable=Marital_Status_radio, value="Single")
R3.grid(row=1, column=6, sticky='w')
R4 = Radiobutton(per_info_frame, text="Married", variable=Marital_Status_radio, value="Married")
R4.grid(row=2, column=6, sticky='w')
R5 = Radiobutton(per_info_frame, text="Divorced", variable=Marital_Status_radio, value="Divorced")
R5.grid(row=3, column=6, sticky='w')
corps_label = tkinter.Label(per_info_frame, text="Corps")
corps_label.grid(row=2, column=0)
Corps = StringVar()
corps_entry = tkinter.Entry(per_info_frame, textvariable=Corps)
corps_entry.grid(row=3, column=0)
appointment_label = tkinter.Label(per_info_frame, text="Appointment")
appointment_label.grid(row=2, column=1)
Appointment = StringVar()
appointment_entry = tkinter.Entry(per_info_frame, textvariable=Appointment)
appointment_entry.grid(row=3, column=1)
deploy_label = tkinter.Label(per_info_frame, text="Deployment")
deploy_label.grid(row=2, column=2)
Deployment = StringVar()
deploy_entry = tkinter.Entry(per_info_frame, textvariable=Deployment)
deploy_entry.grid(row=3, column=2)
state_label = tkinter.Label(per_info_frame, text="State")
state_label.grid(row=2, column=3)
State = StringVar()
state_entry = ttk.Combobox(per_info_frame, values=["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa",
                                                   "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti",
                                                   "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano",
                                                   "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
                                                   "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto",
                                                   "Taraba", "Yobe", "Zamfara"], state="readonly", textvariable=State)
state_entry.grid(row=3, column=3)
trade_label = tkinter.Label(per_info_frame, text="Trade Class")
trade_label.grid(row=2, column=4)
Trade = StringVar()
trade_entry = tkinter.Entry(per_info_frame, textvariable=Trade)
trade_entry.grid(row=3, column=4)
address_label = tkinter.Label(per_info_frame, text="Accommodation Address")
address_label.grid(row=4, column=0, columnspan=2)
address_entry = tkinter.Text(per_info_frame, width=10, height=10, padx=3, pady=2, wrap=WORD)
address_entry.grid(row=5, column=0, columnspan=2, sticky="new")
per_img_frame = Frame(per_info_frame, bg="black", width=300, height=310, borderwidth=3, relief=GROOVE)
per_img_frame.grid(row=5, column=4, columnspan=2)
img = Image.open("fotos/passport.png")
resized_image = img.resize((300, 310))
photo = ImageTk.PhotoImage(resized_image)
img_label = Label(per_img_frame, image=photo)
img_label.place(x=0, y=0)
serial_label = tkinter.Label(per_info_frame, text="Serial No.", font="13")
serial_label.grid(row=4, column=6)
Serial_Number = IntVar()
serial_number_entry = tkinter.Entry(per_info_frame, textvariable=Serial_Number, font="13", state="readonly", width=5, bd=5,
                                    justify=RIGHT)
serial_number_entry.grid(row=5, column=6, sticky='n')


# Buttons
upload_image_btn = tkinter.Button(per_info_frame, text="Upload\nImage", command=upload_img, bg='lightblue')
upload_image_btn.grid(row=5, column=3, sticky='e')
clear_image_btn = tkinter.Button(per_info_frame, text="Clear\nImage", command=clear_image, bg='lightpink')
clear_image_btn.grid(row=5, column=3, sticky='se')
clear_button = tkinter.Button(per_info_frame, text="CLEAR ALL", command=clear_all_fields, bg='#eb8080')
clear_button.grid(row=6, column=0, sticky='news', padx=20, pady=2)
register_personnel_btn = tkinter.Button(per_info_frame, text="REGISTER PERSONNEL", command=reg_per, bg='lightgreen')
register_personnel_btn.grid(row=7, column=0, sticky='news', padx=20, pady=2)
update_button = tkinter.Button(per_info_frame, text="UPDATE INFORMATION", bg='#a980eb', command=update_record)
update_button.grid(row=8, column=0, sticky='news', padx=20, pady=2)
return_button = tkinter.Button(per_info_frame, text="Go Back", command=go_back, bg="#ce7e00")
return_button.grid(row=9, column=0, sticky='news', padx=20, pady=2)

# Peruse database buttons
peruse_db_frame = tkinter.Button(per_info_frame, text="PERUSE DATABASE", bg="#45818e", command=peruse_database)
peruse_db_frame.grid(row=9, column=1)
icon1 = PhotoImage(file="icons/arrow-left-bold-circle-outline.png")
icon2 = PhotoImage(file="icons/arrow-right-bold-circle-outline.png")
go_back_btn = tkinter.Button(per_info_frame, image=icon1, command=previous_personnel)
go_back_btn.grid(row=9, column=2, sticky='w')
go_forward_btn = tkinter.Button(per_info_frame, image=icon2, command=next_personnel)
go_forward_btn.grid(row=9, column=2, sticky='e')

# Search Widgets
find_label = tkinter.Label(per_info_frame, text='Find:', font='bold 13')
find_label.grid(row=7, column=3, sticky='w')
search_string_entry = tkinter.Entry(per_info_frame, font='13')
search_string_entry.grid(row=8, column=3, sticky='w')
search_icon = PhotoImage(file="icons/search.png")
name_search_btn = tkinter.Button(per_info_frame, text="Search NAME", image=search_icon, bg="#a3c2c2", compound=RIGHT)
name_search_btn.grid(row=6, column=4, sticky='news')
army_number_search_btn = tkinter.Button(per_info_frame, text="Search ARMY NUMBER", image=search_icon, bg="#a3c2c2", compound=RIGHT)
army_number_search_btn.grid(row=7, column=4, sticky='news')
rank_search_btn = tkinter.Button(per_info_frame, text="Search RANK", image=search_icon, bg="#a3c2c2", compound=RIGHT)
rank_search_btn.grid(row=8, column=4, sticky='news')
unit_search_btn = tkinter.Button(per_info_frame, text="Search UNIT", image=search_icon, bg="#a3c2c2", compound=RIGHT)
unit_search_btn.grid(row=9, column=4, sticky='news')
trade_search_btn = tkinter.Button(per_info_frame, text="Search TRADE", image=search_icon, bg="#a3c2c2", compound=RIGHT)
trade_search_btn.grid(row=6, column=5, columnspan=2, sticky='news')
corps_search_btn = tkinter.Button(per_info_frame, text="Search CORPS", image=search_icon, bg="#a3c2c2", compound=RIGHT)
corps_search_btn.grid(row=7, column=5, columnspan=2, sticky='news')
appt_search_btn = tkinter.Button(per_info_frame, text="Search APPOINTMENT", image=search_icon, bg="#a3c2c2", compound=RIGHT)
appt_search_btn.grid(row=8, column=5, columnspan=2, sticky='news')
deployment_search_btn = tkinter.Button(per_info_frame, text="Search GENDER", image=search_icon, bg="#a3c2c2", compound=RIGHT)
deployment_search_btn.grid(row=9, column=5, columnspan=2, sticky='news')

for widget in per_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=2)

window.mainloop()

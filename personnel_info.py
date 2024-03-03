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
window.geometry("1150x650")
window.resizable(False, False)

# Main Frame
frame = tkinter.Frame(window)
frame.pack()


# Function to select image file from os
# and display on form selected image
def upload_img():
    global img_label
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Photo File", filetypes=(("JPG File", "*.jpg"),
                                                                                                        ("PNG File", "*.png"),
                                                                                                        ("All Files", "*.txt")))
    img_name = Image.open(filename)
    resized_photo = img_name.resize((300, 310))
    photo2 = ImageTk.PhotoImage(resized_photo)
    img_label.config(image=photo2)
    img_label = photo2


def clear_image():
    global img_label
    img_label = Label(per_img_frame, image=photo)
    img_label.place(x=0, y=0)


def gender_selection():
    global gender
    value = radio.get()
    if value == 1:
        gender = "Male"
    else:
        gender = "Female"


def marital_status_check():
    global marital_stats
    value1 = radio.get()
    if value1 == 1:
        marital_stats = "Single"
    elif value1 == 2:
        marital_stats = "Married"
    elif value1 == 3:
        marital_stats = "Divorced"


# Function to collect personnel information into database
# and create one if one doesn't exist
def reg_per():
    if army_no_entry.get() == "" or rank_entry.get() == "" or first_name_entry.get() == "" or last_name_entry.get()\
       == "" or unit_entry.get() == "" or corps_entry.get() == "" or appt_entry.get() == "" or deploy_entry.get()\
       == "" or state_entry.get() == "" or trade_entry.get() == "" or address_entry.get("1.0", 'end') == "":
        tkinter.messagebox.showinfo(title="ERROR", message="Please all fields are required to be filled")
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
        try:
            sex = gender
        except NameError:
            tkinter.messagebox.showerror("Error", "Please select Gender")
        unit = unit_entry.get()
        corps = corps_entry.get()
        appointment = appt_entry.get()
        deployment = deploy_entry.get()
        state = state_entry.get()
        trade = trade_entry.get()
        address = address_entry.get("1.0", 'end-1c')
        try:
            marital_status = marital_stats
        except NameError:
            tkinter.messagebox.showerror("Error", "Please Select Marital Status")
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
    appt_entry.delete(0, 'end')
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


# Frame to collect all required information
per_info_frame = tkinter.LabelFrame(frame, text="Personnel Information")
per_info_frame.grid(row=0, column=0)

# Labels and Entries
army_no_label = tkinter.Label(per_info_frame, text="Army Number")
army_no_label.grid(row=0, column=0)
army_no_entry = tkinter.Entry(per_info_frame)
army_no_entry.grid(row=1, column=0)
rank_label = tkinter.Label(per_info_frame, text="Rank")
rank_label.grid(row=0, column=1)
rank_entry = ttk.Combobox(per_info_frame, values=["Brig Gen", "Col", "Lt Col", "Maj", "Capt", "Lt", "2Lt", "AWO", "MWO",
                                                  "WO", "SSgt", "Sgt", "Cpl", "LCpl", "Pte"], state="readonly")
rank_entry.grid(row=1, column=1)
first_name_label = tkinter.Label(per_info_frame, text="First Name")
first_name_label.grid(row=0, column=2)
first_name_entry = tkinter.Entry(per_info_frame)
first_name_entry.grid(row=1, column=2)
last_name_label = tkinter.Label(per_info_frame, text="Last Name")
last_name_label.grid(row=0, column=3)
last_name_entry = tkinter.Entry(per_info_frame)
last_name_entry.grid(row=1, column=3)
unit_label = tkinter.Label(per_info_frame, text="Unit")
unit_label.grid(row=0, column=4)
unit_entry = tkinter.Entry(per_info_frame)
unit_entry.grid(row=1, column=4)
gender_label = tkinter.Label(per_info_frame, text="Gender")
gender_label.grid(row=0, column=5)
radio = IntVar()
R1 = Radiobutton(per_info_frame, text="Male", variable=radio, value=1, command=gender_selection)
R1.grid(row=1, column=5, sticky='w')
R2 = Radiobutton(per_info_frame, text="Female", variable=radio, value=2, command=gender_selection)
R2.grid(row=2, column=5, sticky='w')
status_label = tkinter.Label(per_info_frame, text="Marital Status")
status_label.grid(row=0, column=6)
radio1 = IntVar()
R3 = Radiobutton(per_info_frame, text="Single", variable=radio1, value=1, command=marital_status_check)
R3.grid(row=1, column=6, sticky='w')
R4 = Radiobutton(per_info_frame, text="Married", variable=radio1, value=2, command=marital_status_check)
R4.grid(row=2, column=6, sticky='w')
R5 = Radiobutton(per_info_frame, text="Divorced", variable=radio1, value=3, command=marital_status_check)
R5.grid(row=3, column=6, sticky='w')
corps_label = tkinter.Label(per_info_frame, text="Corps")
corps_label.grid(row=2, column=0)
corps_entry = tkinter.Entry(per_info_frame)
corps_entry.grid(row=3, column=0)
appt_label = tkinter.Label(per_info_frame, text="Appointment")
appt_label.grid(row=2, column=1)
appt_entry = tkinter.Entry(per_info_frame)
appt_entry.grid(row=3, column=1)
deploy_label = tkinter.Label(per_info_frame, text="Deployment")
deploy_label.grid(row=2, column=2)
deploy_entry = tkinter.Entry(per_info_frame)
deploy_entry.grid(row=3, column=2)
state_label = tkinter.Label(per_info_frame, text="State")
state_label.grid(row=2, column=3)
state_entry = ttk.Combobox(per_info_frame, values=["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa",
                                                   "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti",
                                                   "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano",
                                                   "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa", "Niger",
                                                   "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto",
                                                   "Taraba", "Yobe", "Zamfara"], state="readonly")
state_entry.grid(row=3, column=3)
trade_label = tkinter.Label(per_info_frame, text="Trade Class")
trade_label.grid(row=2, column=4)
trade_entry = tkinter.Entry(per_info_frame)
trade_entry.grid(row=3, column=4)
address_label = tkinter.Label(per_info_frame, text="Accommodation Address")
address_label.grid(row=4, column=0, columnspan=2)
address_entry = Text(per_info_frame, width=10, height=10, padx=3, pady=2, wrap=WORD)
address_entry.grid(row=5, column=0, columnspan=2, sticky="ew")
per_img_frame = Frame(per_info_frame, bg="black", width=300, height=310, borderwidth=3, relief=GROOVE)
per_img_frame.grid(row=5, column=4, columnspan=2)
img = Image.open("fotos/passport.png")
resized_image = img.resize((300, 310))
photo = ImageTk.PhotoImage(resized_image)
img_label = Label(per_img_frame, image=photo)
img_label.place(x=0, y=0)


# Buttons
upload_image_btn = tkinter.Button(per_info_frame, text="Upload\nImage", command=upload_img, bg='lightblue')
upload_image_btn.grid(row=5, column=3, sticky='e')
clear_image_btn = tkinter.Button(per_info_frame, text="Clear\nImage", command=clear_image, bg='lightpink')
clear_image_btn.grid(row=5, column=3, sticky='se')
clear_button = tkinter.Button(per_info_frame, text="CLEAR ALL", command=clear_all_fields, bg='#eb8080')
clear_button.grid(row=6, column=0, sticky='news', padx=20, pady=2)
register_personnel = tkinter.Button(per_info_frame, text="REGISTER PERSONNEL", command=reg_per, bg='lightgreen')
register_personnel.grid(row=7, column=0, sticky='news', padx=20, pady=2)
update_button = tkinter.Button(per_info_frame, text="UPDATE INFORMATION", bg='#a980eb')
update_button.grid(row=8, column=0, sticky='news', padx=20, pady=2)
return_button = tkinter.Button(per_info_frame, text="Go Back", command=go_back, bg="#ce7e00")
return_button.grid(row=9, column=0, sticky='news', padx=20, pady=2)

for widget in per_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=2)

window.mainloop()

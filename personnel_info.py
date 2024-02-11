import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

# Defining  necessary image variables
img_name = ""
per_image = ['images/blank.jpg']


# Function to clear all input fields at will
def clear_all_fields():
    global img
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
    status_entry.set('')
    img = ""
    return


def clear_image():
    global img
    img = ""


# Function to collect personnel information into database
# and create one if one doesn't exist
def reg_per():
    global img
    if army_no_entry.get() == "" or rank_entry.get() == "" or first_name_entry.get() == "" or last_name_entry.get()\
        == "" or unit_entry.get() == "" or corps_entry.get() == "" or appt_entry.get() == "" or deploy_entry.get()\
        == "" or state_entry.get() == "" or trade_entry.get() == "" or address_entry.get("1.0", 'end') == "" or\
            status_entry.get() == "" or img_name == "":
        tkinter.messagebox.showinfo(title="ERROR", message="Please all fields are required to be filled")
    else:
        # User Info
        with open(img_name, 'rb') as file:
            photo_image = file.read()
        armynumber = army_no_entry.get()
        rank = rank_entry.get()
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()
        unit = unit_entry.get()
        corps = corps_entry.get()
        appointment = appt_entry.get()
        deployment = deploy_entry.get()
        state = state_entry.get()
        trade = trade_entry.get()
        address = address_entry.get("1.0", 'end-1c')
        maritalstatus = status_entry.get()
        image = photo_image

        # Create Table
        conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Personnel_Info (armynumber TEXT, rank TEXT, firstname TEXT,
        lastname TEXT, unit TEXT, corps TEXT, appointment TEXT, deployment TEXT, state TEXT, trade TEXT, 
        address TEXT, maritalstatus TEXT, image BLOB)
        '''
        conn.execute(table_create_query)

        # Insert Data
        data_insert_query = '''INSERT INTO Personnel_Info (armynumber, rank, firstname, lastname, unit, corps, appointment,
        deployment, state, trade, address, maritalstatus, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        data_insert_tuple = (armynumber, rank, firstname, lastname, unit, corps, appointment, deployment, state, trade,
                             address, maritalstatus, image)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()

        # Notify info entry success
        tkinter.messagebox.showinfo(title="DONE", message="Personnel has been registered successfully")

        # Clear fields
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
        status_entry.set('')
        img = ""
        return


# Function to return to DB Hub (close dialog box at the moment)
def go_back():
    window.destroy()
    pass


# Main Window
window = tkinter.Tk()
window.title("Personnel Entry Form")
window.geometry("900x600")
window.resizable(False, False)

# Main Frame
frame = tkinter.Frame(window)
frame.pack()


# Function to select image file from os
# and display on form selected image
def upload_img():
    global per_image
    global img
    global img_name
    img_name = filedialog.askopenfilename()
    per_image.append(img_name)
    per_img_frame_canvas.pack()
    img = ImageTk.PhotoImage(Image.open(per_image[len(per_image) - 1]))
    per_img_frame_canvas.create_image(20, 20, anchor='nw', image=img)


# Frame to collect all required information
per_info_frame = tkinter.LabelFrame(frame, text="Personnel Information")
per_info_frame.grid(row=0, column=0, padx=20, pady=10, ipady=10)

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
address_entry = Text(per_info_frame, width=10, height=10, padx=5, pady=5, wrap=WORD)
address_entry.grid(row=5, column=0, columnspan=2, sticky="ew")
status_label = tkinter.Label(per_info_frame, text="Marital Status")
status_label.grid(row=4, column=2)
status_entry = ttk.Combobox(per_info_frame, values=["Single", "Married", "Divorced"], state="readonly")
status_entry.grid(row=5, column=2, sticky='n')
per_img_label = tkinter.Label(per_info_frame, text="Personnel Photo")
per_img_label.grid(row=4, column=3, columnspan=2)
per_img_frame = tkinter.LabelFrame(per_info_frame, text='Photo', width=300, height=250, borderwidth=3, relief=GROOVE)
per_img_frame.grid(row=5, column=3, columnspan=2)
per_img_frame_canvas = tkinter.Canvas(per_img_frame, bg='grey', width=300, height=250, scrollregion=(0, 0, 500, 500))
per_img_frame_canvas.pack(expand=True, fill='both')
per_img_frame_canvas.bind('<Button-4>', lambda event: per_img_frame_canvas.yview_scroll(int(event.y / 90), "units"))
per_img_frame_canvas.bind('<Button-5>', lambda event: per_img_frame_canvas.yview_scroll(-int(event.y / 90), "units"))
per_img_frame_canvas_scrollbar = ttk.Scrollbar(per_img_frame, orient='vertical', command=per_img_frame_canvas.yview)
per_img_frame_canvas_scrollbar_btn = ttk.Scrollbar(per_img_frame, orient='horizontal', command=per_img_frame_canvas.xview)
per_img_frame_canvas.configure(yscrollcommand=per_img_frame_canvas_scrollbar.set,
                               xscrollcommand=per_img_frame_canvas_scrollbar_btn.set)
per_img_frame_canvas_scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
per_img_frame_canvas_scrollbar_btn.place(relx=0, rely=1, relwidth=1, anchor='sw')


# Buttons
upload_image_btn = tkinter.Button(per_info_frame, text="Upload\nImage", command=upload_img)
upload_image_btn.grid(row=5, column=2, sticky='e')
clear_image_btn = tkinter.Button(per_info_frame, text="Clear\nImage", command=clear_image)
clear_image_btn.grid(row=5, column=2, sticky='se')
clear_button = tkinter.Button(frame, text="CLEAR ALL", command=clear_all_fields)
register_personnel = tkinter.Button(frame, text="REGISTER PERSONNEL", command=reg_per)
return_button = tkinter.Button(frame, text="Go Back", command=go_back)
clear_button.grid(row=1, column=0, sticky='news', padx=20, pady=2)
register_personnel.grid(row=2, column=0, sticky='news', padx=20, pady=2)
return_button.grid(row=3, column=0, sticky='news', padx=20, pady=2)

for widget in per_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=2)

window.mainloop()

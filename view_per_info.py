from customtkinter import *
from PIL import Image
import sqlite3
import io


conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("SELECT * FROM Personnel_Info")
r = c.fetchall()
i = 0


app = CTk()
app.geometry("360x640")
app.title("Personnel Information")

set_appearance_mode("dark")

# Heading
heading = CTkLabel(master=app, font=("Roboto", 17, "italic"), text="Personnel Information", text_color="#ba862c")
heading.place(x=90, y=5)

# Image
photo = r[i][14]
# convert image data to file object
fp = io.BytesIO(photo)
per_image = CTkImage(dark_image=Image.open(fp), size=(200, 200))
image_label = CTkLabel(master=app, image=per_image, text="")
image_label.place(x=10, y=40)


# Buttons
def next_per():
    global i
    global photo
    global fp
    global per_image
    i += 1
    photo = r[i][14]
    fp = io.BytesIO(photo)
    per_image = CTkImage(dark_image=Image.open(fp), size=(200, 200))
    image_label.configure(image=per_image)
    army_number_label.configure(text=r[i][1])
    rank_label.configure(text=r[i][2])
    first_name_label.configure(text=r[i][3])
    last_name_label.configure(text=r[i][4])
    per_state_label.configure(text=r[i][10])
    per_unit_label.configure(text=r[i][6])
    per_corps_label.configure(text=r[i][7])
    per_deployment_label.configure(text=r[i][9])
    per_appointment_label.configure(text=r[i][8])
    per_trade_label.configure(text=r[i][11])
    per_marital_status_label.configure(text=r[i][13])
    per_address_label.configure(text=r[i][12])


def go_back():
    app.destroy()
    pass


edit_btn = CTkButton(master=app, text="EDIT PER DATA", corner_radius=32, fg_color="#815337", hover_color="#ab8a76",
                     border_color="#f7e5da", border_width=1, font=("Roboto", 12, "italic"))
edit_btn.place(x=215, y=40)
next_per_btn = CTkButton(master=app, text="NEXT PER", corner_radius=32, fg_color="#815337", hover_color="#ab8a76",
                         border_color="#f7e5da", border_width=1, font=("Roboto", 12, "italic"), command=next_per)
next_per_btn.place(x=215, y=120)
exit_btn = CTkButton(master=app, text="GO BACK", corner_radius=32, fg_color="#815337", hover_color="#ab8a76",
                     border_color="#f7e5da", border_width=1, font=("Roboto", 12, "italic"), command=go_back)
exit_btn.place(x=215, y=200)

# Labels
army_number_label = CTkLabel(master=app, font=("Roboto", 19, "italic", "bold"), text=r[i][1], text_color="#ba862c")
army_number_label.place(x=10, rely=.38)
rank_label = CTkLabel(master=app, font=("Roboto", 19, "italic", "bold"), text=r[i][2], text_color="#ba862c")
rank_label.place(x=10, rely=.43)
first_name_label = CTkLabel(master=app, font=("Roboto", 19, "italic", "bold"), text=r[i][3], text_color="#ba862c")
first_name_label.place(x=10, rely=.48)
last_name_label = CTkLabel(master=app, font=("Roboto", 19, "italic", "bold"), text=r[i][4], text_color="#ba862c")
last_name_label.place(relx=.45, rely=.48)
state_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="State:", text_color="#ba862c")
state_label.place(x=10, rely=.53)
per_state_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][10], text_color="#ba862c")
per_state_label.place(x=90, rely=.53)
unit_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Unit:", text_color="#ba862c")
unit_label.place(x=10, rely=.58)
per_unit_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][6], text_color="#ba862c")
per_unit_label.place(x=90, rely=.58)
corps_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Corps:", text_color="#ba862c")
corps_label.place(x=10, rely=.63)
per_corps_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][7], text_color="#ba862c")
per_corps_label.place(x=90, rely=.63)
deployment_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Deployment:", text_color="#ba862c")
deployment_label.place(x=10, rely=.68)
per_deployment_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][9], text_color="#ba862c")
per_deployment_label.place(x=150, rely=.68)
appointment_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Appointment:", text_color="#ba862c")
appointment_label.place(x=10, rely=.73)
per_appointment_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][8], text_color="#ba862c")
per_appointment_label.place(x=150, rely=.73)
trade_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Trade:", text_color="#ba862c")
trade_label.place(x=10, rely=.78)
per_trade_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][11], text_color="#ba862c")
per_trade_label.place(x=90, rely=.78)
marital_status_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Marital Status:", text_color="#ba862c")
marital_status_label.place(x=10, rely=.83)
per_marital_status_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][13], text_color="#ba862c")
per_marital_status_label.place(x=165, rely=.83)
address_label = CTkLabel(master=app, font=("Roboto", 17, "italic", "bold"), text="Accommodation:", text_color="#ba862c")
address_label.place(x=10, rely=.865)
per_address_label = CTkLabel(master=app, font=("Roboto", 17, "italic"), text=r[i][12],
                             text_color="#ba862c", wraplength=200, justify='left')
per_address_label.place(x=165, rely=.87)


app.mainloop()

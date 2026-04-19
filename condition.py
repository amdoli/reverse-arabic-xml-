import tkinter as tk
import json
import sys
import subprocess
from xmlrev import Config

def install_Package(package):
    print(f"installing {package}........")
    subprocess.check_call([sys.executable,"-m","pip","install",package])

try:
    import customtkinter as ctk
except ModuleNotFoundError:
    install_Package("customtkinter")

conf=Config()
data=conf.load_json()

all_except=data["method"]["all_except"]
only=data["method"]["only"]
print(f"all={all_except} only={only}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# start the engine
root = ctk.CTk()
root.title("Configuration")
root.geometry('500x650')

def switch():
    if switch_all.get() == "on":
        data["method"]["all_except"] = True
        if data["method"]["only"] == True:
            data["method"]["only"] = False
            switch_only.set("off")
    else:
        data["method"]["all_except"] = False
        
    if switch_only.get() == "on":
        data["method"]["only"] = True
        if data["method"]["all_except"] == True:
            data["method"]["all_except"] = False
            switch_all.set("off")
    else:
        data["method"]["only"] = False
    
    if checkbox_reshape.get() == True:
        data["features"]["reshape"] = True
    else:
        data["features"]["reshape"] = False
    
    if checkbox_reverse.get() == True:
        data["features"]["reverse"] = True
    else:
        data["features"]["reverse"] = False

    conf.save(data)

def button_event():
    print("hello world")

# Switch boxes
switch_all = ctk.StringVar(value="on" if all_except else "off")
switch_only = ctk.StringVar(value="on" if only else "off")

switch_1 = ctk.CTkSwitch(root, variable=switch_all, onvalue="on", offvalue="off", command=switch, text="ALL_EXCEPT")
switch_1.pack(pady=10)

switch_2 = ctk.CTkSwitch(root, variable=switch_only, onvalue="on", offvalue="off", command=switch, text="ONLY")
switch_2.pack()

# Checkboxes
checkbox_reshape = ctk.BooleanVar(value=True if data["features"]["reshape"] else False)
checkbox_reverse = ctk.BooleanVar(value=True if data["features"]["reverse"] else False)


checkbox_reshape = ctk.CTkCheckBox(root, text="Reshape", variable=checkbox_reshape, onvalue=True, offvalue=False, command=switch)
checkbox_reshape.pack()

checkbox_reverse = ctk.CTkCheckBox(root, text="Reverse", variable=checkbox_reverse, onvalue=True, offvalue=False, command=switch)
checkbox_reverse.pack()


root.mainloop()



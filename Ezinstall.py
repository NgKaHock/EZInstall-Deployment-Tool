import customtkinter as ctk
from PIL import Image
import subprocess
import tkinter as tk
import threading


#theme
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")  


#Window setup
app = ctk.CTk()
app.title("EZinstall by Ka Hock")
app.geometry("700x900") # 宽 x 高

# software list 
apps ={
    "Chrome" : {"type":"winget", 
                "id": "Google.Chrome",
                "logo":"image/Google.png" },

    "Acrobat" : {"type":"winget",
                "id":"Adobe.Acrobat.Reader.64-bit", 
                "logo":"image/Acrobat.png"},

    "Anydesk" : {"type":"winget", 
                 "id":"AnyDesk.AnyDesk", 
                 "logo":"image/Anydesk.png"},

    "Click Share":{"type":"exe", 
                   "path":"Installer/ClickShare.exe", 
                   "args": ["/S"], 
                   "logo":"image/ClickShare.png"},  #Company Stuff

    "Eshare" :{"type":"winget", 
               "id":"EShare.EShare", 
               "logo":"image/Eshare.png"},

    "Forticlient":{"type":"exe",  
                   "path":"Installer/FortiClientInstaller.exe", 
                   "args": ["/quiet", "/norestart"], 
                   "logo":"image/Forticlient.png"},

    "MoM Smart Client Printer":{"type":"msi", 
                                "path":"Install/MomSmartClient_x64.msi_windows_x64_2024.2.1.3.msi", 
                                "logo":"image/uniflow.png"},  #Company Stuff

    "Sogou Mandirn Keyboard":{"type":"winget", 
                              "id":"Sogou.SogouInput", 
                              "logo":"image/Sogou.png"},

    "Microsoft Teams":{"type":"winget", 
                       "id":"Microsoft.Teams.Free", 
                       "logo":"image/Microsoft Teams.png"},

    "Team Viewer":{"type":"winget", 
                   "id":"TeamViewer.TeamViewer", 
                   "logo":"image/Team Viewer.png"},

    "Office LTSC Standard Installer":{"type":"exe", 
                                      "path":"Install/setup.exe", 
                                      "args": ["/configure configuration.xml"], 
                                      "logo":"image/Office L.png"},  #Company Stuff

    "Whatsapp":{"type":"exe",  
                "path":"Installer/WhatsAppInstaller.exe",
                "args": ["/S"], 
                "logo":"image/Whatsapp.png"},

    "Wechat":{"type":"winget", 
              "id":"Tencent.WeChat.Universal", 
              "logo":"image/Wechat.png"},

    "Visual Studio Code":{"type":"winget", 
                          "id":"Microsoft.VisualStudioCode", 
                          "logo":"image/Visual Studio Code.jpg"}
}

preset = {
    "New laptop" : ["Chrome", "Acrobat", "Anydesk", "Click Share", "Eshare", "Forticlient", "MoM Smart Client Printer", "Sogou Mandirn Keyboard", "Microsoft Teams", "Team Viewer", "Office LTSC Standard Installer"],

}

# 存 check box
checkboxes={}


# title
title = ctk.CTkLabel(
    app, 
    text="Welcome to EZinstall!! ",
    font=("Segoe UI", 30,"bold")
)

title.pack(pady=(20,10))

subtitle = ctk.CTkLabel(
    app,
    text="Select the software you want to install",
    font=("Segoe UI", 16)
)
subtitle.pack(pady=(0,20))

# progress bar
progress = ctk.CTkProgressBar(app,width=400)
progress.pack(pady=10)
progress.set(0)

#frame
scroll_frame = ctk.CTkScrollableFrame(
    app,
    width=500,
    height=300
    )
scroll_frame.pack( pady=10)

# app card 
for index,(app_name, app_info) in enumerate(apps.items()):

    row = index // 2
    col = index % 2

    card = ctk.CTkFrame(
        scroll_frame,
        corner_radius=15
    )

    card.grid(
        row=row,
        column=col,
        padx=10,
        pady=10,
        sticky="ew"
    )

    image = ctk.CTkImage(
        light_image = Image.open(app_info["logo"]),
        size = (35,35)
    )

    logo=ctk.CTkLabel(
        card, 
        image=image,
        text=""
    )
    logo.pack(side="left", padx=10)

    checkbox = ctk.CTkCheckBox(
        card,
        text=app_name,
        font=("Segoe UI", 14)
    )

    checkbox.pack(side="left",padx=10)

    checkboxes[app_name] = checkbox

def set_ui_state(state:bool):

    for cb in checkboxes.values():
        cb.configure(state="disabled" if not state else "normal") 

    select_button.configure(state="disabled" if not state else "normal")
    deselect_button.configure(state="disabled" if not state else "normal")
    preset_button.configure(state="disabled" if not state else "normal")
    install_button.configure(state="disabled" if not state else "normal")

# preset dropdown
def apply_preset(preset_name):

    for cb in checkboxes.values():
        cb.deselect()

    # choose the apps in the preset
    for app_name in preset[preset_name]:
        if app_name in checkboxes:
            checkboxes[app_name].select()

        write_log(f"Preset applied : {preset_name}")

# log function
def write_log(msg):
    def _write():

        global log_box  
        try:
            if (log_box is not None and log_box.winfo_exists()):
                log_box.insert("end",msg + "\n")
                log_box.see("end")

        except:
            pass

    app.after(0,_write)


def install():

    def run():
        app.after(0, lambda: set_ui_state(False))
        app.after(0, lambda: write_log("Starting installation....."))

        selected_apps = []

        for app_name, app_info in apps.items():

            if checkboxes[app_name].get():
                selected_apps.append((app_name,app_info))

        total = len(selected_apps)

        if total == 0 :
            app.after(0,lambda: write_log("Nothing selected, Please select an application."))
            return
        current = 0
        for app_name, app_info, in selected_apps:
                app.after(0, lambda n=app_name: write_log(f"installing {n}...."))
                try:
                    if app_info["type"]== "winget":
                        result=subprocess.run(
                            ["winget", "install", app_info["id"], "-e"],
                            input="Y\n",
                            capture_output=True,
                            text=True,
                            shell=True
                        )
                    # EXE
                    elif app_info["type"] == "exe":

                        cmd = [app_info["path"]]

                        if "args" in app_info:
                            cmd.extend(app_info["args"])

                        result=subprocess.run(
                            cmd,
                            capture_output=True,
                            input="Y\n",
                            text=True,
                            shell=True
                        )
                    # MSI
                    elif app_info["type"]== "msi":
                        result=subprocess.run(
                            ["msiexec",
                            "/i",
                            app_info["path"],
                                "/qn"
                            ],
                            capture_output=True,
                            input="Y\n",
                            text=True,
                            shell=True
                        )

                    if result.returncode == 0:
                        app.after(0,lambda n=app_name: write_log(f"SUCCESS : {n}"))
                    else:
                        app.after(0, lambda n=app_name:write_log(f"FAILED : {n}"))

                except Exception as e:
                    app.after(0,lambda n=app_name, err=str(e): write_log(f"ERROR: {n} - {err}"))

                current += 1
                progress_value=current/ total

                app.after(0,lambda v=progress_value: progress.set(v))

                app.after(0,lambda: write_log(f"{app_name} installed successfully!"))
        app.after(0, lambda: write_log("Installation completed!"))
        app.after(0, lambda: set_ui_state(True))

    threading.Thread(target=run,daemon=True).start()


# button 
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=15)

# select all
def select_all():

    for checkbox in checkboxes.values():
        checkbox.select()

# delect all
def deselect_all():
    for checkbox in checkboxes.values():
        checkbox.deselect()

#buttons function
select_button= ctk.CTkButton(
    button_frame,
    text="Select All",
    command=lambda: threading.Thread(target=select_all).start()
)
select_button.pack(side="left", padx=5)

deselect_button = ctk.CTkButton(
    button_frame,
    text="Deselect All",
    command=lambda: threading.Thread(target=deselect_all).start() 
)
deselect_button.pack(side='left', padx=5)

# preset button

preset_button = ctk.CTkButton(
    button_frame,
    text = "New laptop preset",
    command=lambda: apply_preset("New Laptop")
)
preset_button.pack(side="left", padx=5)

install_button = ctk.CTkButton(
    app, 
    text="Install",
    height=40,
    width=200,
    command=lambda:threading.Thread(target=install).start()
)
install_button.pack(pady=10)

log_box = ctk.CTkTextbox(
    app,
    width=650,
    height=150,
    font=("Consolas", 12)
)
log_box.pack(pady=10)


app.mainloop()
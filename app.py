import io
import base64
import modules.dbm as dbm
import modules.dbm as local_dbm
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk,Image
from pathlib import Path

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.default_size = "750x300"
        self.title("chat app")
        self.geometry("500x520")
        self.iconphoto(False,tk.PhotoImage(file="assets/img/logo.png"))
        self.visible_frame = None
        self.switch_window(Splash_screen)
             
    def switch_window(self, new_frame):
        if self.visible_frame is not None:
            self.visible_frame.destroy()
        self.visible_frame = new_frame(self)
        self.visible_frame.grid(column = 1, row = 1)


class Splash_screen(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.img = ImageTk.PhotoImage(Image.open("assets/img/logo.png").resize((500,480)))
        self.labell = ttk.Label(self, image=self.img)
        self.labell.pack()
        self.loading_label = ttk.Label(self,text="Loading...", font=("Arial",18))
        self.loading_label.pack()
        self.master.after(5000,lambda: self.master.switch_window(login_window))

class login_window(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.master.geometry = self.master.default_size
        self.header_label = ttk.Label(self, text = "LOGIN", font=("Arial",12,"bold","underline")).grid(column=0,row=0,columnspan=3)

        self.username_label = ttk.Label(self, text = "Username", font=("Arial",11,"bold")).grid(column=0,row=1)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1,row=1,columnspan=2,sticky="ew")

        self.user_does_not_exist = ttk.Label(self,text="User does not exist",foreground=("#ff0000"))

        self.password_label = ttk.Label(self, text = "Password", font=("Arial",11,"bold")).grid(column=0,row=2)
        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(column=1,row=2,columnspan=2,sticky="ew")

        self.password_is_wrong = ttk.Label(self,text="The password is wrong",foreground=("#ff0000"))

        self.sign_up_button = ttk.Button(self,text = "Sign up", command=lambda: master.switch_window(sign_up_window)).grid(column=1,row=3)
        self.login_button = ttk.Button(self,text="Login", command=self.submit_form).grid(column=2,row=3)
    
    def submit_form(self):
        try:
            state = dbm.verify_password("Username",self.username_entry.get(),self.password_entry.get())
            if state == 0:
                self.user_does_not_exist.destroy()
                self.password_is_wrong.grid(column=3,row=2)
            elif state == 1:
                user_data = dbm.get_user_details(self.username_entry.get())
                state_2 = local_dbm.add_user(user_data["first_name"],user_data["second_name"],user_data["username"],user_data["age"],user_data["password"],user_data["email"],user_data["profile_photo"])
                self.master.switch_window(Main_menu)
            elif state == 2:
                self.password_is_wrong.destroy()
                self.user_does_not_exist.grid(column=3,row=1)
        except:
            pass

class sign_up_window(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.header_label = ttk.Label(self, text = "Sign Up", font=("Arial",12,"bold","underline")).grid(column=0,row=0,columnspan=3)

        self.profile_picture = ImageTk.PhotoImage(Image.open("assets/img/profile_placeholder.jpg").resize((40,40)))
        self.profile_picture_button = ttk.Button(self, image=self.profile_picture, command=self.pick_image)
        self.profile_picture_button.grid(column=1,row=2,columnspan=3)

        self.first_name_label = ttk.Label(self, text = "Name", font=("Arial",11,"bold")).grid(column=0,row=3)
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(column=1,row=3,columnspan=1)
        
        self.second_name_entry = ttk.Entry(self)
        self.second_name_entry.grid(column=2,row=3,columnspan=1)
        
        self.email_label = ttk.Label(self, text = "Email", font=("Arial",11,"bold")).grid(column=0,row=4)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(column=1,row=4,columnspan=2,sticky="ew")
        
        self.username_label = ttk.Label(self, text = "Username", font=("Arial",11,"bold")).grid(column=0,row=5,)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1,row=5,columnspan=2,sticky="ew")

        self.age_label = ttk.Label(self, text = "Age", font=("Arial",11,"bold")).grid(column=0,row=6)
        self.age_entry = ttk.Entry(self)
        self.age_entry.grid(column=1,row=6,columnspan=2,sticky="ew")
        
        self.password_label = ttk.Label(self, text = "Password", font=("Arial",11,"bold")).grid(column=0,row=7)
        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(column=1,row=7,columnspan=2,sticky="ew")
        
        self.login_button = ttk.Button(self,text="Login",command=lambda: master.switch_window(login_window)).grid(column=1,row=8,sticky="ew")
        self.sign_up_button = ttk.Button(self,text = "Sign up",command=self.submit_form).grid(column=2,row=8,sticky="ew")

    def convert_image_into_binary(self, decoded_image):
        file = open(decoded_image, 'rb')
        binary = file.read()
        binary = base64.b64encode(binary)
        return binary
    
    def pick_image(self):
        self.profile_select_dialogue = filedialog.askopenfilenames(title="SELECT IMAGE", filetypes=( ("png","*png"), ("Jpg","*.jpg"), ("Allfile","*.*")))
        self.profile_picture = ImageTk.PhotoImage(Image.open(self.profile_select_dialogue[0]).resize((40,40)))
        self.profile_picture_button.config(image = self.profile_picture)

    def submit_form(self):
        try:
            self.profile_picture_bin = self.convert_image_into_binary(self.profile_select_dialogue[0])
            state = dbm.add_user(self.first_name_entry.get(),self.second_name_entry.get(),self.username_entry.get(),int(self.age_entry.get()),self.password_entry.get(),self.email_entry.get(),self.profile_picture_bin)
            if state == 1:
                self.master.switch_window(Main_menu)
            else:
                print("User not added")
        except:
            print("Error")

class Main_menu(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.visible_frame = None
        self.menu_bar = tk.Menu(self)
        #self.menu_icon = ImageTk.PhotoImage(Image.open("assets/img/logo.png").resize((50,50)))
        #self.menu_icon = ImageTk.PhotoImage(Image.open(io.BytesIO(self.convert_binary_into_image(dbm.get_user_details("ouma")["profile_photo"]))).resize((50,50)))
        #self.menu_bar.add_command(image=self.menu_icon)
        #self.master.config(menu = self.menu_bar)

        self.side_bar = ttk.Frame(self)
        self.side_bar.grid(column=0,row=0,sticky="nsew")

        self.account_img_bin = self.convert_binary_into_image(dbm.get_user_details("ouma")["Profile_photo"])
        self.menu_icon_bin = ImageTk.PhotoImage(Image.open(io.BytesIO(self.account_img_bin)).resize((50,50)))
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(column=1,row=0,sticky="nsew")
        self.side_bar_user_icon = ttk.Button(self.side_bar, image=self.menu_icon_bin, command=lambda: self.switch_window(Account_setting_window))
        self.side_bar_user_icon.grid(column=0,row=0)

        #self.side_bar_frame

    def switch_window(self, new_frame):
        if self.visible_frame is not None:
            self.visible_frame.destroy()
        self.visible_frame = new_frame(self)
        self.visible_frame.grid(column = 1, row = 1)

    def convert_binary_into_image(self, image_binary):
        image_binary_decoded = base64.b64decode((image_binary))
        sth = open("temp_img.png","wb")
        sth.write(image_binary_decoded)
        return image_binary_decoded


class Account_setting_window(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.header_label = ttk.Label(self, text = "Sign Up", font=("Arial",12,"bold","underline")).grid(column=0,row=0,columnspan=3)

        self.profile_picture = ImageTk.PhotoImage(Image.open("assets/img/profile_placeholder.jpg").resize((40,40)))
        self.profile_picture_button = ttk.Button(self, image=self.profile_picture, command=self.pick_image)
        self.profile_picture_button.grid(column=1,row=2,columnspan=3   )

        self.first_name_label = ttk.Label(self, text = "Name", font=("Arial",11,"bold")).grid(column=0,row=3)
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(column=1,row=3,columnspan=1)
        
        self.second_name_entry = ttk.Entry(self)
        self.second_name_entry.grid(column=2,row=3,columnspan=1)
        
        self.email_label = ttk.Label(self, text = "Email", font=("Arial",11,"bold")).grid(column=0,row=4)
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(column=1,row=4,columnspan=2,sticky="ew")
        
        self.username_label = ttk.Label(self, text = "Username", font=("Arial",11,"bold")).grid(column=0,row=5,)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(column=1,row=5,columnspan=2,sticky="ew")

        self.age_label = ttk.Label(self, text = "Age", font=("Arial",11,"bold")).grid(column=0,row=6)
        self.age_entry = ttk.Entry(self)
        self.age_entry.grid(column=1,row=6,columnspan=2,sticky="ew")
        
        self.password_label = ttk.Label(self, text = "Password", font=("Arial",11,"bold")).grid(column=0,row=7)
        self.password_entry = ttk.Entry(self)
        self.password_entry.grid(column=1,row=7,columnspan=2,sticky="ew")
        
        self.login_button = ttk.Button(self,text="Login",command=lambda: master.switch_window(login_window)).grid(column=1,row=8,sticky="ew")
        self.sign_up_button = ttk.Button(self,text = "Sign up",command=self.submit_form).grid(column=2,row=8,sticky="ew")

    def convert_image_into_binary(self, decoded_image):
        file = open(decoded_image, 'rb')
        binary = file.read()
        binary = base64.b64encode(binary)
        return binary
    
    def pick_image(self):
        self.profile_select_dialogue = filedialog.askopenfilenames(title="SELECT IMAGE", filetypes=( ("png","*png"), ("Jpg","*.jpg"), ("Allfile","*.*")))
        self.profile_picture = ImageTk.PhotoImage(Image.open(self.profile_select_dialogue[0]).resize((40,40)))
        self.profile_picture_button.config(image = self.profile_picture)

    def submit_form(self):
        try:
            self.profile_picture_bin = self.convert_image_into_binary(self.profile_select_dialogue[0])
            state = dbm.add_user(self.first_name_entry.get(),self.second_name_entry.get(),self.username_entry.get(),int(self.age_entry.get()),self.password_entry.get(),self.email_entry.get(),self.profile_picture_bin)
            if state == 1:
                self.master.switch_window(Main_menu)
            else:
                print("User not added")
        except:
            print("Error")


if __name__ == "__main__":
    try:
        app = App()
        app.mainloop()
    except:
        pass
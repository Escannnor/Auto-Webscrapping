# import sqlite3
# import requests
# from bs4 import BeautifulSoup



# base_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=samsung+s21&_sacat=0&_pgn='
# n = range(1, 10)
# for num in n:
#     url = f'{base_url}{num}'
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     for data in soup.find_all('li', {'class': 's-item s-item__pl-on-bottom'}):
#         product_name = data.find('span', {'role': 'heading'})
#         name = product_name.text.strip()
#         fig = data.find('span', {'class': 's-item__price'})
#         price = fig.text.strip()
#         img = data.find('img')
#         if img:
#             image = img.get('src')
        
#         info = data.find('span', {'class': 'SECONDARY_INFO'})
#         detail = info.text.strip()
#         link = data.find('a')
#         if link:
#             url =  link.get('href')


# def create():
#     connection = sqlite3.connect('product.db')
#     cursor = connection.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS product (
#                         id INTEGER PRIMARY KEY,
#                         name TEXT,
#                         price TEXT,
#                         url TEXT,
#                         image TEXT,
#                         detail TEXT)''')
#     connection.commit()
#     connection.close()



import customtkinter as ctk
import requests
from tkinter import messagebox

BASE_URL = "http://localhost:8000"  # Adjust this to match your API's base URL

class APIClient:
    @staticmethod
    def login(username, password):
        url = f"{BASE_URL}/token"
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Login failed: {response.text}")

    @staticmethod
    def signup(username, email, password):
        url = f"{BASE_URL}/user/signup"
        data = {"username": username, "email": email, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Signup failed: {response.text}")

class BaseApp(ctk.CTk):
    def __init__(self, title, geometry="1200x700"):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_input_frame(self, parent, label_text, show=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family="Helvetica", size=20))
        label.grid(row=0, column=0, sticky="nw")
        entry = ctk.CTkEntry(frame, width=400, height=60, show=show, placeholder_text=f"enter your {label_text.lower()}", font=ctk.CTkFont(family="Helvetica", size=20))
        entry.grid(row=1, column=0)
        return frame

class HoverFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = kwargs.get('fg_color', 'white')

    def on_enter(self, event):
        self.configure(border_width=2, border_color="#3B3BFF")

    def on_leave(self, event):
        self.configure(border_width=0)

class LoginApp(BaseApp):
    def __init__(self):
        super().__init__("Login Screen")
        self.create_login_frame()
        self.create_right_frame()

    def create_login_frame(self):
        login_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
        login_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        login_frame.grid_rowconfigure(4, weight=1)
        login_frame.grid_columnconfigure(0, weight=1)

        login_label = ctk.CTkLabel(login_frame, text="Sign In", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), text_color="blue")
        login_label.grid(row=0, column=0, padx=40, pady=30, sticky="nw")

        self.username_frame = self.create_input_frame(login_frame, "Username")
        self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="nw")

        self.password_frame = self.create_input_frame(login_frame, "Password", show="•")
        self.password_frame.grid(row=2, column=0, padx=40, pady=(0, 10), sticky="nw")

        login_button = ctk.CTkButton(login_frame, text="Sign In", command=self.login_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        login_button.grid(row=5, column=0, padx=40, pady=(2, 20))

    def create_right_frame(self):
        right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        welcome_label = ctk.CTkLabel(right_frame, text="Welcome Back!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
        welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

        sub_label = ctk.CTkLabel(right_frame, text="Please Sign in to Continue.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

        signup_label = ctk.CTkLabel(right_frame, text="New to Data Hive?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        signup_label.grid(row=2, column=0, padx=40, pady=(80, 0))

        signup_button = ctk.CTkButton(right_frame, text="Sign Up", command=self.show_signup_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        signup_button.grid(row=3, column=0, padx=40, pady=(30, 120))

    def login_event(self):
        username = self.username_frame.winfo_children()[1].get()
        password = self.password_frame.winfo_children()[1].get()
        try:
            token = APIClient.login(username, password)
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.destroy()
            DataHiveApp(token, username).mainloop()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def show_signup_page(self):
        self.destroy()
        SignUpApp().mainloop()

class SignUpApp(BaseApp):
    def __init__(self):
        super().__init__("Sign Up Page")
        self.create_signup_frame()
        self.create_right_frame()

    def create_signup_frame(self):
        signup_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
        signup_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        signup_frame.grid_rowconfigure(5, weight=1)
        signup_frame.grid_columnconfigure(0, weight=1)

        signup_label = ctk.CTkLabel(signup_frame, text="Sign Up", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"))
        signup_label.grid(row=0, column=0, padx=40, pady=30)

        self.username_frame = self.create_input_frame(signup_frame, "Username")
        self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 20))

        self.email_frame = self.create_input_frame(signup_frame, "Email")
        self.email_frame.grid(row=2, column=0, padx=40, pady=(0, 20))

        self.password_frame = self.create_input_frame(signup_frame, "Password", show="•")
        self.password_frame.grid(row=3, column=0, padx=40, pady=(0, 20))

        signup_button = ctk.CTkButton(signup_frame, text="Sign Up", command=self.signup_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        signup_button.grid(row=4, column=0, padx=40, pady=(20, 20))

    def create_right_frame(self):
        right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        welcome_label = ctk.CTkLabel(right_frame, text="Welcome to Data Hive!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
        welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

        sub_label = ctk.CTkLabel(right_frame, text="Please Sign up to get started.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

        login_label = ctk.CTkLabel(right_frame, text="Already have an account?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        login_label.grid(row=2, column=0, padx=40, pady=(80, 0))

        login_button = ctk.CTkButton(right_frame, text="Sign In", command=self.show_login_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        login_button.grid(row=3, column=0, padx=40, pady=(30, 120))

    def signup_event(self):
        username = self.username_frame.winfo_children()[1].get()
        email = self.email_frame.winfo_children()[1].get()
        password = self.password_frame.winfo_children()[1].get()
        try:
            APIClient.signup(username, email, password)
            messagebox.showinfo("Signup Successful", "Account created successfully!")
            self.show_login_page()
        except Exception as e:
            messagebox.showerror("Signup Failed", str(e))

    def show_login_page(self):
        self.destroy()
        LoginApp().mainloop()

class DataHiveApp(BaseApp):
    def __init__(self, token, username):
        super().__init__(f"Welcome to Data Hive, {username}!")
        # Implement your main application logic here

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()


# def add_data():
#     connection = sqlite3.connect('product.db')
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO product VALUES ('{name}','{price}', '{url}', '{image}', '{detail}')")
#     connection.commit()
#     connection.close()
#     return "Product saved"

# print(create(), add_data())
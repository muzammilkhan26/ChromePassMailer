# ChromePassMailer

## Description
ChromePassMailer is a Python program that automates the process of extracting Chrome passwords and sending them via email. It uses the `os`, `json`, `base64`, `sqlite3`, `win32crypt`, `Cryptodome.Cipher`, `shutil`, `pandas`, `datetime`, `smtplib`, `email.mime.multipart`, `email.mime.base`, `email`, `socket`, and `getpass` libraries to achieve this functionality.

## Installation
1. First, ensure you have Python installed on your system.
2. Clone or download the repository containing the `requirements.txt` file and the Python script.
3. Navigate to the project directory using the command line.
4. Install the required dependencies by running the following command:
```pip install -r requirements.txt```

## Usage
1. After installing the dependencies, you can run the Python script.
2. The program will extract Chrome passwords and save them in an Excel file named `chrome_passwords.xlsx`.
3. It will then send the Excel file as an email attachment to the specified recipient.
4. Make sure to provide the necessary input such as email content, recipient address, etc., as prompted by the program.
5. Ensure that you have a stable internet connection while running the program to send emails successfully.
6. Be cautious while entering sensitive information such as email credentials to prevent unauthorized access.

## Note
- The program is designed to work on Windows operating systems.
- It is recommended to run the program on a secure and trusted environment.
- Use the program responsibly and in compliance with applicable laws and regulations.
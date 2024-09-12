import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime
import os
import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="12345",
        database="gym"
    )

def register_attendance(mobile_no):
    # Path to the new CSV file for attendance records
    csv_file_path = r'C:\Users\Aman\Desktop\gym2\key.csv'
    
    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_file_path)
    
    # Read the existing data if the file exists
    if file_exists:
        df = pd.read_csv(csv_file_path)
    else:
        # Create a new DataFrame with the required columns if the file does not exist
        df = pd.DataFrame(columns=['Mobile No', 'Name', 'Time'])
    
    conn = connect_db()
    cursor = conn.cursor()

    # Query to get the member details based on mobile number
    query = "SELECT name FROM members WHERE mobile_no = %s"
    cursor.execute(query, (mobile_no,))
    result = cursor.fetchone()

    if result:
        name = result[0]  # Fetch the name from the result
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Prepare the data to save in DataFrame
        attendance_data = {
            'Mobile No': [mobile_no],
            'Name': [name],
            'Time': [current_time]
        }

        # Append the new data to the DataFrame
        new_df = pd.DataFrame(attendance_data)
        df = pd.concat([df, new_df], ignore_index=True)

        # Write the updated DataFrame to the CSV file
        df.to_csv(csv_file_path, index=False)
        
        messagebox.showinfo("Success", f"Attendance registered for {name}")
    else:
        messagebox.showerror("Error", f"No member found with mobile number: {mobile_no}")

    cursor.close()
    conn.close()

def submit():
    mobile_no = entry_mobile.get()
    if not mobile_no:
        messagebox.showerror("Input Error", "Please enter a mobile number.")
    else:
        register_attendance(mobile_no)

# Tkinter GUI setup
root = tk.Tk()
root.title("Gym Attendance System")
root.geometry("400x200")
root.configure(bg="#f0f8ff")

# Font settings
font_title = ('Helvetica', 16, 'bold')
font_label = ('Helvetica', 12)
font_button = ('Helvetica', 12, 'bold')

# Layout frames
frame = tk.Frame(root, padx=20, pady=20, bg="#e6f7ff", borderwidth=2, relief="solid")
frame.pack(padx=20, pady=20)

# Title label
label_title = tk.Label(frame, text="Gym Attendance System", font=font_title, bg="#e6f7ff", fg="#003366")
label_title.grid(row=0, column=0, columnspan=2, pady=10)

# Mobile number input
label_mobile = tk.Label(frame, text="Enter Mobile Number:", font=font_label, bg="#e6f7ff", fg="#003366")
label_mobile.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

entry_mobile = tk.Entry(frame, font=font_label, width=20)
entry_mobile.grid(row=1, column=1, padx=5, pady=5)

# Submit button
submit_button = tk.Button(frame, text="Submit", command=submit, font=font_button, bg="#4CAF50", fg="white", padx=10, pady=5)
submit_button.grid(row=2, columnspan=2, pady=10)

# Run the application
root.mainloop()
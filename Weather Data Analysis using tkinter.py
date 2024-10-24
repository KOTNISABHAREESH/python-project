import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

data = pd.read_csv('temperature.csv')
data['Unnamed: 0'] = data['Unnamed: 0'].str.strip()

for col in data.columns[1:]:
    data[col] = pd.to_numeric(data[col], errors='coerce')

root = tk.Tk()
root.title("Temperature Data Visualization")
root.geometry("400x350")
root.configure(bg="#1E1E1E")

# Load the background image
bg_image = tk.PhotoImage(file="cloud.png")
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

# Function to update and display current time
def update_time():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    time_label.after(1000, update_time)  # Update the time every second

time_label = tk.Label(root, fg="white", bg="#1E1E1E", font=("Arial", 10))
time_label.pack(pady=5)
update_time()

heading_label = tk.Label(root, text="Weather Analysis Using Bar Graph", fg="black"
                         , font=("Arial", 16, "bold"))
heading_label.pack(pady=10)

def show_histogram():
    selected_state = state_combobox.get()
    if selected_state == "":
        messagebox.showerror("Error", "Please select a state.")
        return
    
    temperatures = data.loc[data['Unnamed: 0'] == selected_state].values[0][1:]
    months = data.columns[1:]

    if temperatures.size == 0 or any(pd.isna(temperatures)):
        messagebox.showerror("Error", "Invalid temperature data for the selected state.")
        return

    plt.figure(figsize=(6, 4))
    plt.bar(months, temperatures, color=plt.cm.viridis(range(len(months))), edgecolor='black')
    plt.title(f"Monthly Average Temperatures in {selected_state.capitalize()}", fontsize=12)
    plt.xlabel("Months", fontsize=10)
    plt.ylabel("Temperature (°C)", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def populate_combobox():
    state_names = data['Unnamed: 0'].tolist()
    state_combobox['values'] = state_names

state_label = tk.Label(root, text="Select a State:", bg="#1E1E1E", fg="white"
                       , font=("Arial", 12))
state_label.pack(pady=10)

state_combobox = ttk.Combobox(root, font=("Arial", 10), justify='center')
state_combobox.pack(pady=5)
populate_combobox()

style = ttk.Style()
style.configure("TCombobox", padding=5, font=("Arial", 10), background="#2E2E2E"
                , foreground="black")
style.map("TCombobox", fieldbackground=[("readonly", "#2E2E2E")]
          , background=[("readonly", "#2E2E2E")])

show_button = tk.Button(root, text="Show Histogram", command=show_histogram, bg="#4CAF50"
                        , fg="white", font=("Arial", 10), relief='raised', bd=3)
show_button.pack(pady=20)

footer_label = tk.Label(root, text="Temperature Data Visualization App", bg="#1E1E1E"
                        , fg="white", font=("Arial", 8))
footer_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()

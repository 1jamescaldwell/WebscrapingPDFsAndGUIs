import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import threading

# Function to find PDF links on a webpage using Selenium
def find_pdf_links(url):
    driver = webdriver.Chrome()  # You need to have chromedriver installed and in PATH
    driver.get(url)
    pdf_links = []
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'a[href$=".pdf"]')
        pdf_links = [element.get_attribute('href') for element in elements]
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()
    return pdf_links

# Function to save PDF to a specified directory
def save_pdf(url, directory):
    filename = url.split('/')[-1]  # Extract filename from URL
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)
    print(f"PDF saved: {filename}")

# Function to handle button click event
def download_pdfs():
    model_numbers = entry_model_numbers.get("1.0", tk.END).split()  # Get model numbers from entry widget
    output_directory = entry_output_directory.get()  # Get output directory from entry widget
    total_models = len(model_numbers)
    progress_bar['maximum'] = total_models
    progress_bar['value'] = 0
    progress_label['text'] = f"Downloading PDFs (0/{total_models})"
    for model_number in model_numbers:
        url = "https://www.lego.com/en-us/service/buildinginstructions/" + model_number.strip()
        pdf_links = find_pdf_links(url)
        if pdf_links:
            for pdf_link in pdf_links:
                save_pdf(pdf_link, output_directory)
        else:
            messagebox.showwarning("No PDF Found", f"No PDF found for model number: {model_number}")
        progress_bar['value'] += 1
        progress_label['text'] = f"Downloading PDFs ({progress_bar['value']}/{total_models})"

# Function to handle browse button click event
def browse_output_directory():
    directory = filedialog.askdirectory()
    entry_output_directory.delete(0, tk.END)
    entry_output_directory.insert(0, directory)

# Create GUI window
window = tk.Tk()
window.title("PDF Downloader")
window.geometry("800x400")  # Set window size

# Create labels and entry widgets
label_model_numbers = tk.Label(window, text="Model Numbers (one per line):")
label_model_numbers.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_model_numbers = tk.Text(window, height=10, width=50)
entry_model_numbers.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

label_output_directory = tk.Label(window, text="Output Directory:")
label_output_directory.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_output_directory = tk.Entry(window)
entry_output_directory.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
entry_output_directory.columnconfigure(1, weight=1)  # Allow column 1 to expand

# Create buttons
button_download = tk.Button(window, text="Download PDFs", command=download_pdfs)
button_download.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

button_browse = tk.Button(window, text="Browse", command=browse_output_directory)
button_browse.grid(row=1, column=2, padx=5, pady=5)

# Create progress bar
progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

progress_label = tk.Label(window, text="")
progress_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

# Start GUI event loop
window.mainloop()

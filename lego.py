import tkinter as tk  # Import tkinter module for GUI
from tkinter import messagebox  # Import messagebox for displaying messages
from tkinter import filedialog  # Import filedialog for browsing directories
from tkinter import ttk  # Import ttk for themed widgets
from selenium import webdriver  # Import webdriver from Selenium for web automation
from selenium.webdriver.common.by import By  # Import By for locating elements by various strategies
import requests  # Import requests for making HTTP requests
import os  # Import os for operating system functionalities
import threading  # Import threading for parallel execution

# Function to find PDF links on a webpage using Selenium
def find_pdf_links(url):
    driver = webdriver.Chrome()  # Initialize Chrome webdriver
    driver.get(url)  # Open the URL in Chrome
    pdf_links = []  # Initialize empty list to store PDF links
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, 'a[href$=".pdf"]')  # Find all elements with PDF links
        pdf_links = [element.get_attribute('href') for element in elements]  # Extract PDF links
    except Exception as e:
        print("An error occurred:", e)  # Print error message if any
    finally:
        driver.quit()  # Close the Chrome webdriver
    return pdf_links  # Return list of PDF links

# Function to save PDF to a specified directory
def save_pdf(url, directory):
    filename = url.split('/')[-1]  # Extract filename from URL
    filepath = os.path.join(directory, filename)  # Construct full filepath
    with open(filepath, 'wb') as f:
        response = requests.get(url)  # Get PDF content from URL
        f.write(response.content)  # Write PDF content to file
    print(f"PDF saved: {filename}")  # Print success message

# Function to handle button click event
def download_pdfs():
    model_numbers = entry_model_numbers.get("1.0", tk.END).split()  # Get model numbers from entry widget
    output_directory = entry_output_directory.get()  # Get output directory from entry widget
    total_models = len(model_numbers)  # Get total number of model numbers
    progress_bar['maximum'] = total_models  # Set maximum value for progress bar
    progress_bar['value'] = 0  # Reset progress bar value
    progress_label['text'] = f"Downloading PDFs (0/{total_models})"  # Update progress label
    for model_number in model_numbers:
        url = "https://www.lego.com/en-us/service/buildinginstructions/" + model_number.strip()  # Construct URL
        pdf_links = find_pdf_links(url)  # Find PDF links on webpage
        if pdf_links:
            for pdf_link in pdf_links:
                save_pdf(pdf_link, output_directory)  # Save PDF to output directory
        else:
            messagebox.showwarning("No PDF Found", f"No PDF found for model number: {model_number}")  # Show warning message
        progress_bar['value'] += 1  # Increment progress bar value
        progress_label['text'] = f"Downloading PDFs ({progress_bar['value']}/{total_models})"  # Update progress label

# Function to handle browse button click event
def browse_output_directory():
    directory = filedialog.askdirectory()  # Open directory dialog
    entry_output_directory.delete(0, tk.END)  # Clear output directory entry
    entry_output_directory.insert(0, directory)  # Insert selected directory into entry

# Create GUI window
window = tk.Tk()  # Create tkinter window
window.title("PDF Downloader")  # Set window title
window.geometry("800x400")  # Set window size

# Create labels and entry widgets
label_model_numbers = tk.Label(window, text="Model Numbers (one per line):")  # Create label for model numbers
label_model_numbers.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Place label in grid layout
entry_model_numbers = tk.Text(window, height=10, width=50)  # Create text widget for model numbers
entry_model_numbers.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Place text widget in grid layout

label_output_directory = tk.Label(window, text="Output Directory:")  # Create label for output directory
label_output_directory.grid(row=1, column=0, padx=5, pady=5, sticky="w")  # Place label in grid layout
entry_output_directory = tk.Entry(window)  # Create entry widget for output directory
entry_output_directory.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Place entry widget in grid layout
entry_output_directory.columnconfigure(1, weight=1)  # Allow column 1 to expand

# Create buttons
button_download = tk.Button(window, text="Download PDFs", command=download_pdfs)  # Create button for downloading PDFs
button_download.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Place button in grid layout

button_browse = tk.Button(window, text="Browse", command=browse_output_directory)  # Create button for browsing directory
button_browse.grid(row=1, column=2, padx=5, pady=5)  # Place button in grid layout

# Create progress bar
progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate')  # Create progress bar widget
progress_bar.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")  # Place progress bar in grid layout

progress_label = tk.Label(window, text="")  # Create label for progress status
progress_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")  # Place label in grid layout

# Start GUI event loop
window.mainloop()  # Run tkinter event loop to display GUI

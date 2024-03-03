import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import chromedriver_autoinstaller

# Function to find PDF links on a webpage using Selenium
def find_pdf_links(url):
    chromedriver_autoinstaller.install()

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
    output_directory = r'C:\Users\james.caldwell\Downloads'  # Default output directory
    total_models = len(model_numbers)  # Get total number of model numbers
    progress_bar['maximum'] = total_models * 2 + 1 # Set maximum value for progress bar
    progress_bar['value'] = 0  # Reset progress bar value
    pdf_count = 1
    window.update()  # Update the GUI to reflect changes
    for model_number in model_numbers:
        url = "https://www.lego.com/en-us/service/buildinginstructions/" + model_number.strip()  # Construct URL
        progress_bar['value'] += 1  # Increment progress bar value
        progress_label['text'] = f"({pdf_count}/{total_models}): Searching for {model_number}"  # Update progress label
        window.update()  # Update the GUI to reflect changes
        pdf_links = find_pdf_links(url)  # Find PDF links on webpage
        
        progress_label['text'] = f"({pdf_count}/{total_models}): Saving {model_number}"  # Update progress label
        progress_bar['value'] += 1  # Increment progress bar value
        window.update()  # Update the GUI to reflect changes

        if pdf_links:
            for pdf_link in pdf_links:
                save_pdf(pdf_link, output_directory)  # Save PDF to output directory
        else:
            messagebox.showwarning("No PDF Found", f"No PDF found for model number: {model_number}")  # Show warning message
        # progress_bar['value'] += 1  # Increment progress bar value

        # progress_label['text'] = f"Downloading PDFs ({progress_bar['value']}/{total_models})"  # Update progress label
        # window.update()  # Update the GUI to reflect changes
        pdf_count += 1
    progress_bar['value'] += 1  # Increment progress bar value
    progress_label['text'] = f"Done"  # Update progress label
    window.update()  # Update the GUI to reflect changes

# Function to get the default Downloads folder
def get_default_downloads_folder():
    return os.path.join(os.path.expanduser("~"), "Downloads")

# Function to stop the process
def stop_process():
    window.update()  # Update the GUI to reflect changes
    global stop_process
    stop_process = True
    progress_label['text'] = f"Cancelled"  # Update progress label
    window.update()  # Update the GUI to reflect changes

# Create GUI window
window = tk.Tk()  # Create tkinter window
window.title("PDF Downloader")  # Set window title
window.geometry("800x400")  # Set window size

# Create labels and entry widgets
label_model_numbers = tk.Label(window, text="Model Numbers (one per line):")  # Create label for model numbers
label_model_numbers.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # Place label in grid layout
entry_model_numbers = tk.Text(window, height=10, width=50)  # Create text widget for model numbers
entry_model_numbers.grid(row=0, column=1, padx=5, pady=5, sticky="ew")  # Place text widget in grid layout

label_output_directory = tk.Label(window, text="Output Directory: ")  # Create label for output directory
label_output_directory.grid(row=1, column=0, padx=5, pady=5, sticky="w")  # Place label in grid layout
default_downloads_folder = get_default_downloads_folder()  # Get default Downloads folder
label_downloads_folder = tk.Label(window, text=default_downloads_folder)  # Create label for default Downloads folder
label_downloads_folder.grid(row=1, column=1, padx=5, pady=5, sticky="ew")  # Place label in grid layout

# Create buttons
button_download = tk.Button(window, text="Download PDFs", command=download_pdfs)  # Create button for downloading PDFs
button_download.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Place button in grid layout

# Create progress bar
progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate')  # Create progress bar widget
progress_bar.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")  # Place progress bar in grid layout

progress_label = tk.Label(window, text="")  # Create label for progress status
progress_label.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")  # Place label in grid layout

# Create stop button
button_stop = tk.Button(window, text="Stop", command=stop_process)  # Create button for stopping process
button_stop.grid(row=2, column=2, padx=5, pady=5)  # Place button in grid layout


# Start GUI event loop
window.mainloop()  # Run tkinter event loop to display GUI

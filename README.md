Work in progress 2/26/24

Description
This Python script allows users to download PDF files from webpages containing LEGO building instructions. It utilizes the Selenium library for web automation and tkinter for creating a graphical user interface (GUI). Users can input a list of LEGO set model numbers, specify an output directory, and click a button to download the corresponding PDF files.

Requirements
Python 3.x
Selenium library
Chrome WebDriver
Tkinter library (usually included with Python installation)

Installation
Install Python 3.x from Python.org
Install Selenium library: pip install selenium
Download Chrome WebDriver from ChromeDriver website and add it to your PATH environment variable.
Run the script.

Usage
Launch the script.
Enter LEGO set model numbers into the text area, one per line.
Click the "Browse" button to select the output directory.
Click the "Download PDFs" button to start downloading PDF files.
Progress of downloads will be displayed in the progress bar.

Note
Ensure that the Chrome WebDriver is compatible with your Chrome browser version.
The script may not work if the LEGO website structure changes.

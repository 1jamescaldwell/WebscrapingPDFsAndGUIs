Description
This Python script allows users to download PDF files from webpages containing LEGO building instructions. It utilizes the Selenium library for web automation and tkinter for creating a graphical user interface (GUI). Users can input a list of LEGO set model numbers, specify an output directory, and click a button to download the corresponding PDF files.

Usage:
Run lego.exe
Enter LEGO set model numbers into the text area, one per line.<br>
Default download folder is Downloads. Otherwise, click the "Browse" button to select the output directory.<br>
Click the "Download PDFs" button to start downloading PDF files.<br>
Progress of downloads will be displayed in the progress bar.<br>

Notes: 
* Only works with Google Chrome installed currently.
* Script automatically installs the latest version of Chrome WebDriver, but if your Google Chrome is an older version, install manually from here: Install Chrome WebDriver compatible with your version of Chrome: https://chromedriver.chromium.org/downloads
* The script may not work if the LEGO website structure changes.

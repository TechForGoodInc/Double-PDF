# Double PDF
Application that allows you to scan double-sided documents using a single-sided printer scanner.

Steps to achieve a double-sided PDF:

1. Place the pages (front side) in the printer feeder and make sure the printer scanner outputs into PDF format.
2. After you have finished scanning the front side of the pages, place the pages in the scanner so the printer scans the back sides of the pages.
3. Download the DoublePDF executable and run the program.
4. Click the buttons for the front and back sides and select the front side PDF and the back side PDF.
5. Click submit and the merged file will be in the same directory as the PDF files that you selected. The filename for the merged file will contain the name of the front side PDF, a plus sign, and the name of the back side PDF.


![TroubledRuddy78](https://user-images.githubusercontent.com/18247709/80286901-2e023a80-86fc-11ea-8d46-b79ccd601b11.png)


## Compiling from source code

Required modules:
- PyQT5
- PyPDF2

Double PDF is compiled using pyinstaller with the onefile and noconsole options.

1. Run the following code in the directory where you downloaded the source code in order to get a executable.
`pyinstaller --onefile --noconsole --icon DoublePDF.ico --name DoublePDF  main.py`

2. The dist folder contains the DoublePDF executable.

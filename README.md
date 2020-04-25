# Double PDF
Application that allows you to scan double-sided documents using a single-sided printer scanner.

Steps to achieve a double-sided PDF:

Place the pages (front side) in the printer feeder and make sure the printer scanner outputs into PDF format.
After you have finished scanning the front side of the pages, place the pages in the scanner so the printer scans the back sides of the pages.
Download the DoublePDF file below and run the program.
Click the buttons for the front and back sides and select the front side PDF and the back side PDF.
Click submit and the merged file will be in the same directory as the PDF files that you selected. The filename for the merged file will contain the name of the front side PDF, a plus sign, and the name of the back side PDF.

## Compiling from source code

Required modules:
- PyQT5
- PyPDF2

Double PDF is compiled using pyinstaller with the onefile and noconsole options.

1. Run the following code in the directory where you downloaded the source code in order to get a executable.
`pyinstaller --onefile --noconsole --icon DoublePDF.ico --name DoublePDF  main.py`

2. The dist folder contains the DoublePDF executable.

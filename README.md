# Double PDF
Allows you to scan double-sided documents with a single-sided scanner.

Steps to achieve a double-sided PDF:

1. Place the pages (front side) in the feeder and verify that the scanner outputs into PDF format.
2. After the front-sided scanning is complete, place the pages (back-side) in the feeder.
3. Run DoublePDF.
4. Select the front and back pages pdfs. Click Submit.
5. A new file will appear in the same directory as the program with the following name structure: front_side pdf name plus (+) back_side pdf name. For example, "FrontPages + BackPages".


![TroubledRuddy78](https://user-images.githubusercontent.com/18247709/80286901-2e023a80-86fc-11ea-8d46-b79ccd601b11.png)


## Compiling from source code

Required modules:
- PyQT5
- PyPDF2

Double PDF is compiled using pyinstaller with the onefile and noconsole options.

1. Run the following code in the source code directory:
`pyinstaller --onefile --noconsole --icon DoublePDF.ico --name DoublePDF  main.py`

2. The dist folder will contain the DoublePDF executable.

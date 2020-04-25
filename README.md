# Double PDF
Application that allows you to scan double-sided documents using a single-sided printer scanner.

## Compiling from source code

Required modules:
- PyQT5
- PyPDF2

Double PDF is compiled using pyinstaller with the onefile and noconsole options.

1. Run the following code in the directory where you downloaded the source code in order to get a executable.
`pyinstaller --onefile --noconsole --icon DoublePDF.ico --name DoublePDF  main.py`

2. The dist folder contains the DoublePDF executable.
